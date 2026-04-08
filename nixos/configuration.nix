{ config, pkgs, ... }:

{
  imports = [
      ./hardware-configuration.nix
      ./modules/bundle.nix
      ./modules/services.nix
      ./packages.nix
    ];

  boot.loader.grub.enable = true;
  boot.loader.grub.device = "/dev/vda";
  boot.loader.grub.useOSProber = true;
  

  nix.settings.experimental-features = [ "nix-command" "flakes" ];
  
  boot.kernelPackages = pkgs.linuxPackages_latest;

  networking.hostName = "bedrock";

  networking.networkmanager.enable = true;

  # Define a user account. Don't forget to set a password with ‘passwd’.
  users.users.onicuto = {
    isNormalUser = true;
    description = "onicuto";
    extraGroups = [ "networkmanager" "wheel" ];
    packages = with pkgs; [];
    shell = pkgs.fish;
  };

  programs.fish.enable = true;
	
  programs.hyprland.enable = true;

  # Allow unfree packages
  nixpkgs.config.allowUnfree = true;

  system.stateVersion = "25.11";

}
