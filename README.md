# dotfiles

Personal Linux dotfiles for an Arch Linux desktop built around Hyprland.

## Preview

Screenshots are not included yet. Add them to an `assets/` directory and link them here later.

## Stack

- WM: Hyprland
- Bar: Waybar
- Launcher: Wofi
- Shell: Fish
- Terminal: Ghostty
- Editor: Neovim
- System info: Fastfetch, Neofetch
- TUI tools: Btop, Cava
- File manager config: Thunar
- Themes: GTK 3/4, Qt5ct, Qt6ct, NWG Look
- Icons and cursors: Bibata, MacOS Tahoe, Infinity

## Included

This repository currently tracks:

- `.config/hypr`
- `.config/waybar`
- `.config/wofi`
- `.config/nvim`
- `.config/fish`
- `.config/ghostty`
- `.config/btop`
- `.config/cava`
- `.config/fastfetch`
- `.config/neofetch`
- `.config/gtk-3.0`
- `.config/gtk-4.0`
- `.config/qt5ct`
- `.config/qt6ct`
- `.config/nwg-look`
- `.config/Thunar`
- `.icons`

## Layout

```text
.
├── .config
│   ├── hypr
│   ├── waybar
│   ├── wofi
│   ├── nvim
│   ├── fish
│   ├── ghostty
│   ├── btop
│   ├── cava
│   ├── fastfetch
│   ├── neofetch
│   ├── gtk-3.0
│   ├── gtk-4.0
│   ├── qt5ct
│   ├── qt6ct
│   ├── nwg-look
│   └── Thunar
└── .icons
```

## Notes

- These files are tailored for my machine and workflow.
- The Hyprland setup uses split configs such as `programs.conf`, `binds.conf`, and `windowrules.conf`.
- Fish starts `Hyprland` on `tty1` and `startx` on `tty2`.
- Some values are machine-specific and may need editing before use.
- The Ghostty config uses the `Mellifluous` theme and `JetBrainsMono SemiBold`.
- Waybar is configured with a compact top bar and Hyprland workspace/language modules.

## Install

Clone the repo:

```bash
git clone <your-repo-url> ~/.dotfiles
cd ~/.dotfiles
```

Create symlinks for the configs you want:

```bash
ln -sfn ~/.dotfiles/.config/hypr ~/.config/hypr
ln -sfn ~/.dotfiles/.config/waybar ~/.config/waybar
ln -sfn ~/.dotfiles/.config/wofi ~/.config/wofi
ln -sfn ~/.dotfiles/.config/nvim ~/.config/nvim
ln -sfn ~/.dotfiles/.config/fish ~/.config/fish
ln -sfn ~/.dotfiles/.config/ghostty ~/.config/ghostty
ln -sfn ~/.dotfiles/.icons ~/.icons
```

Create backups first if you already have local configs.

## Dependencies

The setup expects at least some of these packages to be installed:

- `hyprland`
- `waybar`
- `wofi`
- `ghostty`
- `fish`
- `neovim`
- `fastfetch`
- `btop`
- `cava`
- `thunar`
- `qt5ct`
- `qt6ct`
- `nwg-look`

Package names may differ depending on your distribution.

## Arch Packages

Minimal install example:

```bash
sudo pacman -S hyprland waybar wofi ghostty fish neovim fastfetch btop cava thunar qt5ct qt6ct nwg-look
```

Depending on your setup, you may also want:

```bash
sudo pacman -S pavucontrol wl-clipboard grim slurp hyprlock ttf-jetbrains-mono-nerd
```

## Customization

- Edit [`.config/hypr/hyprland.conf`](/home/onicuto/.dotfiles/.config/hypr/hyprland.conf) for monitor, input, animation, and general layout settings.
- Edit [`.config/hypr/binds.conf`](/home/onicuto/.dotfiles/.config/hypr/binds.conf) for keybindings.
- Edit [`.config/waybar/config`](/home/onicuto/.dotfiles/.config/waybar/config) and [`.config/waybar/style.css`](/home/onicuto/.dotfiles/.config/waybar/style.css) for bar modules and styling.
- Edit [`.config/wofi/style.css`](/home/onicuto/.dotfiles/.config/wofi/style.css) for launcher appearance.
- Edit [`.config/fish/config.fish`](/home/onicuto/.dotfiles/.config/fish/config.fish) for aliases, environment variables, and session startup behavior.
- Edit [`.config/ghostty/config`](/home/onicuto/.dotfiles/.config/ghostty/config) for terminal theme, font, and behavior.

## Cleanup

This repository is intended for actual dotfiles only. Cache directories, app binaries, and generated files should stay out of Git history.
