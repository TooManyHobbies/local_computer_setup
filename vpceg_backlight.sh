#!/bin/bash

# Get the user who called this script using sudo. This is
# needed so the i3 scripts are placed in that user's
# home directory.
user=${SUDO_USER:-${USER}}

# Sony Vaio VPCEG Series backlight support
# Create two files that will enable the screen backlight keys (fn F4 and fn F5) to control the screen brightness

# This first file will do the work
printf '#!/bin/bash\n' > /usr/sbin/writeintelbacklight.sh
printf '\n' >> /usr/sbin/writeintelbacklight.sh
printf 'intelmaxbrightness=`cat /sys/class/backlight/intel_backlight/max_brightness`\n' >> /usr/sbin/writeintelbacklight.sh
printf 'acpimaxbrightness=`cat /sys/class/backlight/acpi_video0/max_brightness`\n' >> /usr/sbin/writeintelbacklight.sh
printf 'scale=`expr $intelmaxbrightness / $acpimaxbrightness`\n' >> /usr/sbin/writeintelbacklight.sh
printf 'acpibrightness=`cat /sys/class/backlight/acpi_video0/brightness`\n' >> /usr/sbin/writeintelbacklight.sh
printf 'newintelbrightness=`expr $acpibrightness \* $scale`\n' >> /usr/sbin/writeintelbacklight.sh
printf 'curintelbrightness=`cat /sys/class/backlight/intel_backlight/actual_brightness`\n' >> /usr/sbin/writeintelbacklight.sh
printf 'if [ "$newintelbrightness" -ne "$curintelbrightness" ]\n' >> /usr/sbin/writeintelbacklight.sh
printf 'then\n' >> /usr/sbin/writeintelbacklight.sh
printf '  echo $newintelbrightness >> /sys/class/backlight/intel_backlight/brightness\n' >> /usr/sbin/writeintelbacklight.sh
printf 'fi\n' >> /usr/sbin/writeintelbacklight.sh
printf 'exit 0\n' >> /usr/sbin/writeintelbacklight.sh
printf '\n' >> /usr/sbin/writeintelbacklight.sh

# Redirect system calls to the script above
printf 'ACTION=="change", SUBSYSTEM=="backlight", RUN+="/usr/sbin/writeintelbacklight.sh"\n' > /etc/udev/rules.d/99-writeintelbacklight.rules

# Add support for i3 window manager

mkdir -p /home/$user/.config/i3/actions

# Backlight Donw
printf '#!/bin/sh\n' > /home/$user/.config/i3/actions/bl-down.sh
printf '\n' >> /home/$user/.config/i3/actions/bl-down.sh
printf '# Used for window manager, not Desktop Environment\n' >> /home/$user/.config/i3/actions/bl-down.sh
printf '\n' >> /home/$user/.config/i3/actions/bl-down.sh
printf 'bl_device=/sys/class/backlight/acpi_video0/brightness\n' >> /home/$user/.config/i3/actions/bl-down.sh
printf 'echo $(($(cat $bl_device)-1)) | tee $bl_device\n' >> /home/$user/.config/i3/actions/bl-down.sh

chmod +x /home/$user/.config/i3/actions/bl-down.sh

printf '# Backlight Up\n' > /home/$user/.config/i3/actions/bl-up.sh
printf '#!/bin/sh\n' >> /home/$user/.config/i3/actions/bl-up.sh
printf '\n' >> /home/$user/.config/i3/actions/bl-up.sh
printf '# Used for window manager, not destop environments\n' >> /home/$user/.config/i3/actions/bl-up.sh
printf '\n' >> /home/$user/.config/i3/actions/bl-up.sh
printf 'bl_device=/sys/class/backlight/acpi_video0/brightness\n' >> /home/$user/.config/i3/actions/bl-up.sh
printf 'echo $(($(cat $bl_device)+1)) | tee $bl_device\n' >> /home/$user/.config/i3/actions/bl-up.sh
 
chmod +x /home/$user/.config/i3/actions/bl-up.sh


chown -R $user:$user /home/$user/.config/i3
