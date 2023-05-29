# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'devtoolbox/views')

sources = [
  '__init__.py',
  'tab_content.py',
  'json_yaml.py',
  'timestamp.py',
  'base_converter.py',
  'cron_converter.py',
  'html_encoder.py',
  'url_encoder.py',
  'gzip_compressor.py',
  'jwt_decoder.py',
  'formatter.py',
  'hash_generator.py',
  'lorem_generator.py',
  'uuid_generator.py',
  'text_inspector.py',
  'regex_tester.py',
  'text_diff.py',
  'xml_validator.py',
  'markdown_preview.py',
  'contrast_checker.py',
  'colorblindness_simulator.py',
  'image_converter.py',
  'certificate_parser.py',
  'random_generator.py',
  'certificate_request_generator.py',
  'reverse_cron.py',
  'chmod_calculator.py',
  'qrcode_generator.py',
  'json_validator.py',
]

install_data(sources, install_dir: viewsdir)
