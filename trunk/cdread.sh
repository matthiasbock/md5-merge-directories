#!/bin/bash

$(espeak -v de "CD wird eingelesen. Bitte warten." &> /dev/zero) &
rmdir copy
umount -fl /tmp/mount
sleep 2
rmdir /tmp/mount
rm /tmp/ddrescue.iso
ddrescue /dev/cdrom1 /tmp/ddrescue.iso --max-retries=1 --no-split --verbose
umount -fl /dev/cdrom1
$(espeak -v de "Einlesen abgeschlossen. CD wird ausgeworfen." &> /dev/zero) &
sleep 2
eject /dev/cdrom1
$(espeak -v de "Transferiere die Daten aus dem Abbild auf die Festplatte. Bitte warten." &> /dev/zero) &
chown user.user /tmp/ddrescue.iso
chmod 644 /tmp/ddrescue.iso
mv /tmp/ddrescue.iso /tmp/ddrescue2.iso
mkdir /tmp/mount
mount /tmp/ddrescue2.iso /tmp/mount -o loop
mount /tmp/ddrescue2.iso /tmp/mount -o loop -t iso9660
if [ -e copy ]; then
	cp /tmp/mount copy2 -paR
else
	cp /tmp/mount copy -paR
fi
umount -fl /tmp/mount
rmdir /tmp/mount
chown user.user copy -R
chmod 755 copy -R
$(espeak -v de "Datentransfehr abgeschlossen." &> /dev/zero) &

