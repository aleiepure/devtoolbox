# meson.build
#
# Copyright (C) 2025 Alessandro Iepure
# SPDX-License-Identifier: GPL-3.0-or-later

project('devtoolbox', 'rust', 
  version: '2.0.0',
  meson_version: '>= 1.0.0',
  default_options: [ 'warning_level=2', 'werror=false', ],
)

i18n = import('i18n')
gnome = import('gnome')

subdir('data')
subdir('src')
subdir('po')

install_data('build-aux/devtoolbox-run-script', 
  install_dir: join_paths(get_option('prefix'), meson.project_name())
)

gnome.post_install(
  glib_compile_schemas: true,
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
