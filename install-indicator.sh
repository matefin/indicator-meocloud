#!/bin/bash
# install-indicator.sh
# matefin
# 2014-05-25
# v0.10.02c_00m
#
# installer le cloud storage MEOCloud
#
# https://meocloud.pt/downloads
# http://askubuntu.com/questions/299443/how-do-i-install-copy-file-syncing-software
# http://discourse.ubuntu.com/t/what-are-your-plans-to-replace-ubuntu-one-and-why/1598/20
# http://www.omgubuntu.co.uk/2014/04/three-alternatives-ubuntu-one


#======================================= 
# INITIALISATIONS
#======================================= 
#repertoire de ce script de postinstall
########## A TENIR A JOUR a la main
pidir=$(pwd)

# repertoire courant
curdir=$(pwd)

#==========================================
echo "-- installer le cloud storage MEOCloud

---> veuillez arreter l'indicateur unity MEOCloud s'il est lance

Tapez [Entree] pour continuer"
read bidon

# arreter et tuer meocloud au cas ou il serait lance
# mais l'indicateur va le relancer !!
meocloud stop
sudo killall meocloud

# installer le package de meocloud
cd /tmp
wget -N https://meocloud.pt/binaries/linux/repo/install_meocloud_deb.sh
# patch pour eviter de boucler si erreur de apt-get update
sed "s/retry apt-get update -qq/apt-get update/" \
	install_meocloud_deb.sh > install_meocloud_deb_matefin.sh
cat install_meocloud_deb_matefin.sh | grep "apt-get update"
echo
bash install_meocloud_deb_matefin.sh
cd $curdir
echo "
Tapez [Entree] pour continuer"
read bidon

# installer les icones et regenerer le cache
sudo install -o root -g root -m 644 $pidi/meocloud-icons/*.svg /usr/local/share/pixmaps
sudo gtk-update-icon-cache /usr/local/share/pixmaps

# installer l'indicateur meocloud
sudo install -o root -g root -m 755 $pidir/indicator-meocloud.py /usr/local/bin/

# creer un lanceur pour l'indicateur meocloud
cat << MEOLANC | sudo tee /usr/local/share/applications/meocloud.desktop 1>/dev/null
[Desktop Entry]
Version=1.0
Encoding=UTF-8
Type=Application
Name=MEOCloud
Icon=meocloud-idle.svg
Exec=indicator-meocloud.py
Comment=Sync your files across computers and to the web
Categories=Network;FileTransfer;
Terminal=false
StartupNotify=false
GenericName=File Synchronizer
MEOLANC
#sudo chmod 755 /usr/local/share/applications/meocloud.desktop

echo
echo "--> lancer meocloud pour finir l'installation"
echo
meocloud start

echo
echo "Tapez sur [Entree] pour afficher l'aide de meocloud"
read bidon
# afficher le readme
echo
meocloud -h

echo
echo "---> tapez meocloud dans unity pour lancer l'indicateur meocloud"
echo
echo "Termine [$basename $0]"
exit 0

########## FIN
