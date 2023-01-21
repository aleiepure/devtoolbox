# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
widgetsdir = join_paths(pkgdatadir, 'devtoolbox/widgets')

sources = [
  '__init__.py',
  'utility_title.py',
  'text_area.py',
  'file_viewer.py',
  'text_file_area.py',
  'text_field_action_row.py',
  'sidebar_item.py',
  'binary_selector.py',
]

install_data(sources, install_dir: widgetsdir)
