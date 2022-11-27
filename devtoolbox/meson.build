# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'devtoolbox')

subdir('views')
subdir('widgets')
subdir('services')

sources = [
  '__init__.py',
  'application.py',
  'window.py',
  'utils.py',
]

install_data(sources, install_dir: moduledir)