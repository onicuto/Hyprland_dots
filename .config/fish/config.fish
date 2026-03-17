if status is-interactive
    set -U fish_greeting ""
    fastfetch
    alias py="python3"
    set -xg EDITOR /usr/bin/nvim
    alias vim="nvim"
    alias fishconf="nvim /home/onicuto/.dotfiles/.config/fish/config.fish"
    alias conf="nvim ~/.dotfiles/.config"
    alias lsblk="lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"
    # Commands to run in interactive sessions can go here
end

if test (tty) = /dev/tty1
    exec start-hyprland >/dev/null 2>&1
end
