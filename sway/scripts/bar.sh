#!/bin/bash

# Change this according to your device
################
# Variables
################


# Date and time
date_and_week=$(date "+%m-%d-%Y")
current_time=$(date "+%H:%M")

#############
# Commands
#############

# Battery or charger
battery_charge=$(upower --show-info $(upower --enumerate | grep 'BAT') | egrep "percentage" | awk '{print $2}')
battery_status=$(upower --show-info $(upower --enumerate | grep 'BAT') | egrep "state" | awk '{print $2}')


vpn_name=$(nmcli -t | grep VPN | head -n 1 | cut -d ' ' -f 1)
wifi_up=$(nmcli -t | grep "connected to")
nvpn_up=$(nordvpn status | grep "Connected")
if [ -n "$nvpn_up" ]
then
  vpn_name=$(nordvpn status | grep "City" | cut -d ' ' -f 2-)
fi

bright_time=$(date --date="$(stat ~/.config/sway/bright.txt | grep Modify | cut -d ' ' -f 2-5)" '+%s')
bright_elapsed=$(($bright_time - $(date '+%s')))
brightness_value=$(cat ~/.config/sway/bright.txt | cut -d ',' -f 4) 

packages=$(cat ~/.config/sway/packages.txt 2>/dev/null | wc -l)

# Audio and multimedia
audio_volume=$(pamixer --get-volume)
#audio_volume=$(pamixer --sink `pactl list sinks short | grep RUNNING | awk '{print $1}'` --get-volume)
audio_is_muted=$(pamixer --get-mute)
#audio_is_muted=$(pamixer --sink `pactl list sinks short | grep RUNNING | awk '{print $1}'` --get-mute)
#media_artist=$(playerctl metadata artist)
#media_song=$(playerctl metadata title)
#player_status=$(playerctl status)

# Network
#network=$(ip route get 1.1.1.1 | grep -Po '(?<=dev\s)\w+' | cut -f1 -d ' ')
# interface_easyname grabs the "old" interface name before systemd renamed it
#interface_easyname=$(dmesg | grep $network | grep renamed | awk 'NF>1{print $NF}')
#ping=$(ping -c 1 www.google.es | tail -1| awk '{print $4}' | cut -d '/' -f 2 | cut -d '.' -f 1)
#network=$(curl icanhazip.com)


# Others
#language=$(swaymsg -r -t get_inputs | awk '/1:1:AT_Translated_Set_2_keyboard/;/xkb_active_layout_name/' | grep -A1 '\b1:1:AT_Translated_Set_2_keyboard\b' | grep "xkb_active_layout_name" | awk -F '"' '{print $4}')
#loadavg_5min=$(cat /proc/loadavg | awk -F ' ' '{print $2}')

# Removed weather because we are requesting it too many times to have a proper
# refresh on the bar
#weather=$(curl -Ss 'https://wttr.in/Pontevedra?0&T&Q&format=1')

if [ $battery_status = "discharging" ];
then
    battery_pluggedin='⚠'
else
    battery_pluggedin='⚡'
fi

if [ $audio_is_muted = "true" ]
then
    audio_active='🔇'
else
    audio_active='🔊'
fi

if [ -z "$vpn_name" ]
then
  vpn_active=''
else
  vpn_active='🗝'
fi

if [ -z "$wifi_up" ]
then
  wifi_active='↮'
else
  wifi_active='⇅'
fi

if [ $bright_elapsed -lt -5 ]
then
  brightness=''
else
  brightness="☀ $brightness_value"
fi

if [ $packages -gt 0 ]
then
  packages_prompt="$packages updates"
else
  packages_prompt=''
fi



echo "$brightness   $packages_prompt   $vpn_active $vpn_name   $wifi_active   $audio_active$audio_volume%   $battery_pluggedin$battery_charge   $date_and_week $current_time   "

