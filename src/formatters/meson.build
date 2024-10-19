# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
formattersdir = join_paths(pkgdatadir, 'devtoolbox/formatters')

sources = [
  '__init__.py',
  'formatter.py',
  'json.py',
  'sql.py',
  'xml.py',
  'html.py',
  'js.py',
  'css.py',
  'css_minifier.py',
]

install_data(sources, install_dir: formattersdir)
