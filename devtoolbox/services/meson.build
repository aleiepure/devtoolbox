# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
servicedir = join_paths(pkgdatadir, 'devtoolbox/service')

sources = [
  '__init__.py',
  'base64_encoder.py',
  'cron_parser.py',
  'gzip_encoder.py',
  'html_encoder.py',
  'json_formater.py',
  'json_formater.py',
  'json2yaml.py',
  'jwt_decoder.py',
  'lorem_ipsum_generator.py',
  'number_base.py',
  'sql_formatter.py',
  'url_encoder.py',
  'xml_formatter.py'
]

install_data(sources, install_dir: servicedir)