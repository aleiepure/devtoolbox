# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
pagesdir = join_paths(pkgdatadir, 'devtoolbox/pages')

sources = [
  '__init__.py',
  'utilities_view.py',
  'favorites_view.py'
]

install_data(sources, install_dir: pagesdir)