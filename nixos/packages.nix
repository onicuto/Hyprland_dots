{ pkgs, ... }:

{
  environment.systemPackages = with pkgs; [
    btop
    neofetch
    git
    neovim
    wget
    fish
    openssh
    brightnessctl
    btop  
    cava  
    fastfetch
    stow
    ghostty
    xfce.thunar
    wofi
    blueman


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
    brightnessctl
    btop
    cava
    curl
    eza
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
    
    # Виртуализация
    virt-viewer
    libvirt
    
    # Видео
    vlc
  ];
}
