#!/bin/bash
set -ex

echo "Add verbose debugging" # TODO make configurable
echo auth_verbose = yes >> /etc/dovecot/dovecot.conf 
echo auth_debug = yes >> /etc/dovecot/dovecot.conf 
echo auth_debug_passwords = yes >> /etc/dovecot/dovecot.conf 

echo "Correting directory permissions..."
chown postmaster:postmaster /home/postmaster/Maildir
echo "Starting..."


echo "Compiling config files"
newaliases
postmap /etc/postfix/mydestinations
postmap /etc/postfix/virtual
#dovecot start
/usr/sbin/postfix upgrade-configuration
/usr/sbin/postfix check
/usr/sbin/dovecot
/etc/init.d/postfix start
/etc/init.d/rsyslog start
while [[ ! -f /var/log/syslog ]]; do
    sleep 0.5
done
tail -f /var/log/syslog | grep postfix &
tail -F /var/log/dovecot.log &

set +x
while true;
do
    sleep 10
done

