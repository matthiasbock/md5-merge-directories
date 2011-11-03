#!/bin/bash

dev=$1
saveto=$2

# clean up
rmdir $saveto
umount -fl "/tmp/$dev"
sleep 2
rmdir "/tmp/$dev"
rm /tmp/ddrescue-$dev.iso

# rescue
dd_rescue -v /dev/$dev /tmp/ddrescue-$dev.iso
mv /tmp/ddrescue-$dev.iso /tmp/ddrescue-$dev-finished.iso
chown user.user /tmp/ddrescue-$dev-finished.iso
chmod 644 /tmp/ddrescue-$dev-finished.iso

# finish
umount -fl /dev/$dev
sleep 2
eject /dev/$dev

# move data
mkdir "/tmp/$dev"
mount /tmp/ddrescue-$dev-finished.iso "/tmp/$dev" -o loop -t auto
mount /tmp/ddrescue-$dev-finished.iso "/tmp/$dev" -o loop -t iso9660
if [ -e $saveto ]; then
	cp "/tmp/$dev" "_$saveto" -paR
else
	cp "/tmp/$dev" $saveto -paR
fi
umount -fld "/tmp/$dev"
sleep 2
rmdir "/tmp/$dev"
chown user.user $saveto -R
chmod 755 $saveto -R

