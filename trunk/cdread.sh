#!/bin/bash

dev=$1
saveto=$2

$(espeak -v de "CD wird eingelesen. Bitte warten." &> /dev/zero) &

# clean up
rmdir $saveto
umount -fl "/tmp/$dev"
sleep 2
rmdir "/tmp/$dev"
rm /tmp/ddrescue-$dev.iso

# rescue
ddrescue /dev/$dev /tmp/ddrescue-$dev.iso --max-retries=1 --no-split --verbose
mv /tmp/ddrescue-$dev.iso /tmp/ddrescue-$dev-finished.iso
chown user.user /tmp/ddrescue-$dev-finished.iso
chmod 644 /tmp/ddrescue-$dev-finished.iso

# finish
$(espeak -v de "Einlesen abgeschlossen. CD wird ausgeworfen." &> /dev/zero) &
umount -fl /dev/$dev
sleep 2
eject /dev/$dev

# move data
$(espeak -v de "Transferiere die Daten aus dem Abbild auf die Festplatte. Bitte warten." &> /dev/zero) &
mkdir "/tmp/$dev"
mount /tmp/ddrescue-$dev-finished.iso "/tmp/$dev" -o loop -t auto
mount /tmp/ddrescue-$dev-finished.iso "/tmp/$dev" -o loop -t iso9660
if [ -e $saveto ]; then
	cp "/tmp/$dev" "_$saveto" -paR
else
	cp "/tmp/$dev" $saveto -paR
fi
umount -fl "/tmp/$dev"
rmdir "/tmp/$dev"
chown user.user $saveto -R
chmod 755 $saveto -R

$(espeak -v de "Datentransfehr abgeschlossen." &> /dev/zero) &

