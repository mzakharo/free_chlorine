sudo cp fc.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable fc.service
sudo systemctl start fc.service


