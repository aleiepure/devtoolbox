# Copyright (C) 2022 - 2025 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
compressorsdir = join_paths(pkgdatadir, 'devtoolbox/compressors')

sources = [
  '__init__.py',
  'compressor.py',
  'gzip_compressor.py',
  'lzma_compressor.py',
  'bz2_compressor.py',
]

install_data(sources, install_dir: compressorsdir)
