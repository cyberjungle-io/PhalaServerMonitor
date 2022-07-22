cp rc-local.service /etc/systemd/system
cp rc.local /etc
chmod +x /etc/rc.local

sudo systemctl enable rc-local
sudo systemctl start rc-local.service

chmod +x *.sh