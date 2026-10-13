function git --wraps git --description "Git wrapper with AI commit assistance via agy"
    # Pass through non-commit commands immediately
    if test (count $argv) -eq 0; or test "$argv[1]" != "commit"
        command git $argv
        return $status
    end

    # Pass through in non-interactive sessions or if stdin is not a terminal
    if not status is-interactive; or not isatty stdin
        command git $argv
        return $status
    end

    # Pass through if help is requested
    if contains -- -h $argv; or contains -- --help $argv
        command git $argv
        return $status
    end

    # Pass through if not inside a git repository
    if not command git rev-parse --is-inside-work-tree >/dev/null 2>&1
        command git $argv
        return $status
    end

    # Check if a commit message flag is already provided (-m, -F, --message, --file, etc.)
    set -l has_msg_flag 0
    for arg in $argv[2..-1]
        switch $arg
            case "-m" "-m*" "-F" "-F*" "--message" "--message=*" "--file" "--file=*"
                set has_msg_flag 1
                break
            case "-*m*"
                set has_msg_flag 1
                break
        end
    end

    if test $has_msg_flag -eq 1
        command git $argv
        return $status
    end

    # Check for flags like --amend and -a / --all
    set -l is_amend 0
    set -l is_all 0
    for arg in $argv[2..-1]
        switch $arg
            case "--amend"
                set is_amend 1
            case "-a" "--all" "-*a*"
                set is_all 1
        end
    end

    # Check if there are changes to commit
    if test $is_amend -eq 0
        if test $is_all -eq 1
            if command git diff --quiet 2>/dev/null; and command git diff --cached --quiet 2>/dev/null
                command git $argv
                return $status
            end
        else
            if command git diff --cached --quiet 2>/dev/null
                command git $argv
                return $status
            end
        end
    end

    # Collect diff and summary for agy
    set -l diff_stat ""
    set -l diff_body ""
    if test $is_all -eq 1
        set diff_stat (command git diff HEAD --stat 2>/dev/null; or command git diff --stat 2>/dev/null | string collect)
        set diff_body (command git diff HEAD 2>/dev/null | head -n 350 | string collect; or command git diff 2>/dev/null | head -n 350 | string collect)
    else if test $is_amend -eq 1
        set diff_stat (command git diff HEAD~1 --stat 2>/dev/null; or command git diff --cached --stat 2>/dev/null | string collect)
        set diff_body (command git diff HEAD~1 2>/dev/null | head -n 350 | string collect; or command git diff --cached 2>/dev/null | head -n 350 | string collect)
    else
        set diff_stat (command git diff --cached --stat 2>/dev/null | string collect)
        set diff_body (command git diff --cached 2>/dev/null | head -n 350 | string collect)
    end

    set -l recent_commits (command git log -n 5 --oneline 2>/dev/null | string collect)

    # Generation loop
    while true
        echo (set_color cyan --bold)"Generating commit message with agy..."(set_color normal)

        set -l prompt "You are an expert Git commit assistant.
Generate a strictly single-line, short Conventional Commit message for the following git diff in English.
Format: <type>(<optional-scope>): <short imperative description>
Common types: feat, fix, docs, style, refactor, perf, test, build, ci, chore.

Rules:
1. Output ONLY a single short line. Absolutely no body, no bullet points, no extra lines.
2. Keep it very short and concise (under 60 characters).
3. Do NOT use emojis, symbols, quotes, or markdown blocks.

Recent commits for reference:
$recent_commits

File changes summary:
$diff_stat

Git diff:
$diff_body"

        set -l raw_msg (agy --effort low -p "$prompt" 2>/dev/null | string collect)
        set -l agy_status $status

        if test $agy_status -ne 0; or test -z "$raw_msg"
            echo (set_color red)"Failed to generate message with agy. Falling back to regular git commit."(set_color normal)
            command git $argv
            return $status
        end

        # Take strictly the first non-empty line without code fences
        set -l commit_msg (printf "%s\n" $raw_msg | string match -rv '^```' | string match -rv '^\s*$' | head -n 1 | string trim)
        # Strip enclosing quotes if present
        set commit_msg (string replace -r '^["\'](.*)["\']$' '$1' -- "$commit_msg")

        echo ""
        echo (set_color green --bold)"Proposed commit message:"(set_color normal)
        echo (set_color yellow)"--------------------------------------------------"(set_color normal)
        echo "$commit_msg"
        echo (set_color yellow)"--------------------------------------------------"(set_color normal)
        echo ""

        set -l prompt_text (printf "%s[Y/n/e/r]%s (Enter/y: commit, e: edit, r: retry, n: cancel): " (set_color cyan --bold) (set_color normal))
        read -P "$prompt_text" user_choice
        if test $status -ne 0
            echo ""
            echo (set_color red)"Commit aborted."(set_color normal)
            return 1
        end

        set -l choice (string lower -- (string trim -- "$user_choice"))
        set -l commit_args $argv[2..-1]

        switch "$choice"
            case "" "y" "yes"
                command git commit $commit_args -m "$commit_msg"
                return $status

            case "e" "edit"
                set -l tmp_file (mktemp -t git_commit_msg.XXXXXX)
                printf "%s\n" "$commit_msg" > "$tmp_file"
                set -l editor $EDITOR
                if test -z "$editor"
                    set editor nvim
                end
                eval "$editor \"$tmp_file\""

                if test ! -s "$tmp_file"
                    echo (set_color red)"Aborting commit due to empty message."(set_color normal)
                    rm -f "$tmp_file"
                    return 1
                end

                command git commit $commit_args -F "$tmp_file"
                set -l commit_status $status
                rm -f "$tmp_file"
                return $commit_status

            case "r" "retry"
                echo (set_color magenta)"Regenerating commit message..."(set_color normal)
                continue

            case "*"
                echo (set_color red)"Commit aborted."(set_color normal)
                return 1
        end
    end
end
