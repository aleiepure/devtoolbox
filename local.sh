#!/usr/bin/bash
echo "Uninstalling"
sudo rm -rf /usr/lib/python3.10/site-packages/devtoolbox
sudo rm -rf /usr/share/devtoolbox/
sudo rm /usr/bin/devtoolbox 
echo "Rebuilding"
rm -rf _build/
meson --prefix /usr _build && cd _build
meson compile
echo "Installing"
sudo meson install
cd ..
/usr/bin/devtoolbox
