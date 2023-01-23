# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'devtoolbox')
gnome = import('gnome')

gnome.compile_resources('devtoolbox',
  'devtoolbox.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('debug', get_option('debug'))
if get_option('debug')
  conf.set('app-name', 'Dev toolbox (Development snapshot)')
else
  conf.set('app-name', 'Dev toolbox')
endif

configure_file(
  input: 'devtoolbox.in',
  output: 'devtoolbox',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir')
)

subdir('widgets')
subdir('views')
subdir('services')

devtoolbox_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'utils.py'
]

install_data(devtoolbox_sources, install_dir: moduledir)
