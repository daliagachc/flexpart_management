#!/usr/bin/env bash

name='wrk'
mount_dir='/tmp/taito/'$name
echo $mount_dir
remote_dir='/wrk/aliagadi/DONOTREMOVE'
log_addr='aliagadi@taito-login3.csc.fi'
mkdir -p $mount_dir
umount -f $mount_dir
echo 'cont'
sshfs -oreconnect -o volname=$name $log_addr:$remote_dir $mount_dir

name='home'
mount_dir='/tmp/taito/'$name
remote_dir='/homeappl/home/aliagadi'
log_addr='aliagadi@taito-login3.csc.fi'
mkdir -p $mount_dir
umount -f $mount_dir
echo 'cont'
sshfs -oreconnect -o volname=$name $log_addr:$remote_dir $mount_dir

name='proj'
mount_dir='/tmp/taito/'$name
remote_dir='/proj/atm/saltena'
log_addr='aliagadi@taito-login3.csc.fi'
mkdir -p $mount_dir
umount -f $mount_dir
echo 'cont'
sshfs -oreconnect -o volname=$name $log_addr:$remote_dir $mount_dir

