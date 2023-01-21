# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'devtoolbox/views')

sources = [
  '__init__.py',
  'tab_content.py',
  'favorites.py',
  'json_yaml.py',
]

install_data(sources, install_dir: viewsdir)
