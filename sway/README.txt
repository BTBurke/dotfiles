Add to ~/.config/sway

Add systemd files to ~/.config/systemd/user then
- systemctl --user enable packages.service
- systemctl --user enable packages.timer
- systemctl --user start packages.timer

Also needs AUR packages:
- bemenu
- j4-dmenu-desktop
- pactl
- brightnessctl
- playerctl

