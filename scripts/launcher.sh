#! /bin/bash
export WAYLAND_DISPLAY=wayland-0
export XDG_RUNTIME_DIR=/run/user/$(id -u)
while [ ! -S "$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY" ]; do
    sleep 0.1
done
unclutter -idle 0 &
source /home/west/mri-sim/bin/activate
cd /home/west/uvic-west-fraser-health-MRI-simulator
sudo /home/west/mri-sim/bin/python main.py