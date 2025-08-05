# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
servicesdir = join_paths(pkgdatadir, 'devtoolbox/services')

sources = [
  '__init__.py',
  'json_yaml_toml.py',
  'cron_converter.py',
  'base64_encoder.py',
  'html_encoder.py',
  'url_encoder.py',
  'compressor.py',
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
  'certificate_parser.py',
  'json_validator.py',
]

install_data(sources, install_dir: servicesdir)
