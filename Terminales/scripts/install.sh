sudo apt-get update
sudo apt-get upgrade

sudo apt-get install gnome gimp inkscape geogebra playonlinux openarena
sudo apt-get install python-gst0.10 gstreamer0.10-plugins-base gstreamer0.10-plugins-good gstreamer0.10-plugins-ugly gstreamer0.10-plug$
sudo apt-get install gstreamer0.10-ffmpeg
sudo apt-get install python-gi mplayer gstreamer1.0-tools gir1.2-gstreamer-1.0 gir1.2-gst-plugins-base-1.0 gstreamer1.0-plugins-good gs$

sudo apt-get install ssh chkconfig

ssh-keygen -b 1024 -t rsa -f /etc/ssh/ssh_host_key
ssh-keygen -b 1024 -t rsa -f /etc/ssh/ssh_host_rsa_key
ssh-keygen -b 1024 -t dsa -f /etc/ssh/ssh_host_dsa_key

chkconfig sshd on

sudo nano /etc/ssh/sshd_config

sudo /etc/init.d/ssh restart

sudo apt-get update
sudo apt-get upgrade

gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type string --set /desktop/gnome/background/picture$
gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type string --set /desktop/gnome/interface/gtk_them$
gconftool-2 --direct --config-source xml:readwrite:/etc/gconf/gconf.xml.mandatory --type string --set /desktop/gnome/interface/icon_the$
