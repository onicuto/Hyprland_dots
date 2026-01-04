if status is-interactive
    set -U fish_greeting ""
    fastfetch
    alias py="python3"
    set -xg EDITOR /usr/bin/nvim
    alias vim="nvim"
    alias telefon="scrcpy"
    alias lua="lua5.1"
    alias fishconf="nvim /home/onicuto/.dotfiles/.config/fish/config.fish"
    alias mirrors="sudo reflector --country Russia --age 12 --protocol https --sort rate --save /etc/pacman.d/mirrorlist"
    alias conf="nvim ~/.dotfiles/.config"
    alias xbps-install="sudo xbps-install"
    alias pacman="sudo pacman"
    alias archfetch="brl strat arch ufetch"
    alias voidfetch="brl strat void ufetch"
    # Commands to run in interactive sessions can go here
end

# Created by `pipx` on 2025-11-08 09:42:15
set PATH $PATH /Users/onicuto/.local/bin
