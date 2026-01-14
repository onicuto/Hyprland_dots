# Надо сделать

{
  #fileSystems = {
    "/home/onicuto/HDD" = {
      device = "/dev/disk/by-uuid/55287544-ce9f-4c93-a2f6-a63b69623fe1";
      fsType = "ext4";
      options = [ "defaults" "noatime" ]; #"uid=1000" "gid=1000" "dmask=007" "fmask=117" ];
    };
    "/mnt/shit" = {
      device = "/dev/disk/by-uuid/234dc4ed-ade3-447f-af5a-4d254835cc66";
      fsType = "ext4";
      options = [ "defaults" "noatime" ]; #"uid=1000" "gid=1000" "dmask=007" "fmask=117" ];
    };
  };
}
