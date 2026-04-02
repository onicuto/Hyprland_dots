if status is-interactive
    export LFS=/mnt/lfs
    export FLSH=/run/media/onicuto
    set -U fish_greeting ""
    fastfetch
    alias py="python3"
    set -xg EDITOR /usr/bin/nvim
    alias vim="nvim"
    alias telefon="scrcpy"
    alias lua="lua5.1"
    alias vpip="source ~/.venv/bin/activate.fish"
    alias vpip_exit="deactivate"
    alias fishconf="nvim /home/onicuto/.dotfiles/.config/fish/config.fish"
    alias mirrors="sudo reflector --country Russia --age 12 --protocol https --sort rate --save /etc/pacman.d/mirrorlist"
    alias conf="nvim ~/.dotfiles/.config"
    alias archfetch="brl strat arch ufetch"
    alias voidfetch="brl strat void ufetch"
    alias debfetch="brl strat debian ufetch"
    alias lsblk="lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINT"
    alias brlconf="sudoedit /bedrock/etc/bedrock.conf"
    # Commands to run in interactive sessions can go here
end

if test (tty) = /dev/tty1
    exec start-hyprland >/dev/null 2>&1
end

if test (tty) = /dev/tty2
    startx
end
