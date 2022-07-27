# libadwaita Python Demo

This is a simple demo of using misc. libadwaita widgets from python

Here is the official libadwaita docs.
https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/

## Version

* Version 0.1.0 - The ui is build direct in python : [ver_0.1.0](https://github.com/timlau/adw_pydemo/tree/ver_0.1.0)
* Version 0.2.0 - The ui is build using an .ui file and [Gtk.Template](https://pygobject.readthedocs.io/en/latest/guide/gtk_template.html) 

## Build & Run
Run the following to build, install & run the application on your system
```bash
./local.sh
```

## Flatpak

Enable the [gnome-nightly](https://wiki.gnome.org/Apps/Nightly) flatpak repository
```bash
flatpak remote-add --if-not-exists gnome-nightly https://nightly.gnome.org/gnome-nightly.flatpakrepo
```

Install needed flatpak Platform & SDK
```bash
flatpak install gnome-nightly org.gnome.Platform//master org.gnome.Sdk//master
```

Build flatpak
```bash
flatpak-builder --force-clean .flatpak/repo dk.rasmil.AdwPyDemo.yml
```

Run the flatpak 
```bash
flatpak-builder --run .flatpak/repo dk.rasmil.AdwPyDemo.yml adwpydemo
```

Install to local system & Run it
```bash
flatpak-builder --user --install --force-clean .flatpak/repo dk.rasmil.AdwPyDemo.yml
flatpak run dk.rasmil.AdwPyDemo
```

## Screenshots

![Screenshot from 2021-10-25 14-01-16](https://user-images.githubusercontent.com/283985/138691610-cb20c763-0428-48fe-a826-8196371d30e1.png)
![Screenshot from 2021-10-25 14-01-24](https://user-images.githubusercontent.com/283985/138691699-00531f80-ee33-4aaa-be95-0a2df6b20826.png)
![Screenshot from 2021-10-25 14-01-35](https://user-images.githubusercontent.com/283985/138691724-d4be1ab4-74da-4169-8e72-143c65250a9f.png)
