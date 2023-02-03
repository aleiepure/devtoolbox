# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
servicesdir = join_paths(pkgdatadir, 'devtoolbox/services')

sources = [
  '__init__.py',
  'json_yaml.py',
  'cron_converter.py',
  'html_encoder.py',
  'url_encoder.py',
  'base64_encoder.py',
  'gzip_compressor.py',
]

install_data(sources, install_dir: servicesdir)
