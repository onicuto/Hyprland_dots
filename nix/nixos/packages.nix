{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    btop
    neofetch
    git
    alacritty
    alsa-utils	
    android-tools
    ast-grep
    neovim
    wget
    fish
    openssh
    alacritty
    blueman
    brightnessctl
    btop  
    cava  
    ddcutil 
    kdePackages.dolphin  
    fastfetch
    stow
    alejandra
    onefetch
    atop
    ghostty
    xfce.thunar
    wofi


    # Hyprland
    hypridle
    hyprpolkitagent
    pyprland
    hyprlang
    hyprshot
    hyprcursor
    mesa
    nwg-displays
    nwg-look
    waypaper
    waybar
    
    # Приложения
    power-profiles-daemon
    loupe
    brightnessctl
    btop
    bottom
    cava
    cargo
    cliphist
    cpufrequtils
    curl
    eza
    fastfetch
    git
    grim
    killall
    lazygit
    libnotify
    mpv
    networkmanagerapplet
    pamixer
    pavucontrol
    playerctl
    rofi
    slurp
    swappy
    swww
    wl-clipboard
    wlogout
    
    # Терминалы
    kitty
    
    # Виртуализация
    virt-viewer
    libvirt
    
    # Видео
    vlc
  ];
}
