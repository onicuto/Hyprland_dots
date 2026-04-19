function monitor --description "Set monitor brightness via ddcutil"
    if test (count $argv) -ne 1
        echo "usage: monitor <percent>" >&2
        return 1
    end

    set -l percent $argv[1]

    if not string match -rq '^[0-9]+$' -- $percent
        echo "brightness must be an integer from 0 to 100" >&2
        return 1
    end

    if test $percent -lt 0 -o $percent -gt 100
        echo "brightness must be an integer from 0 to 100" >&2
        return 1
    end

    ddcutil setvcp 10 $percent
end
