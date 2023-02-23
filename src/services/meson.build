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
  'gzip_compressor.py',
  'jwt_decoder.py',
  'hash_generator.py',
  'lorem_generator.py',
  'uuid_generator.py',
  'text_inspector.py',
  'regex_tester.py',
  'text_diff.py',
  'xml_validator.py',
  'markdown_preview.py',
  'colorblindness_simulator.py',
  'image_converter.py',
]

install_data(sources, install_dir: servicesdir)
