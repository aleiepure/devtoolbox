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

if get_option('debug')
  name_suffix = ' (Development snapshot)'

  git = find_program('git', required : false)
  if git.found()
    git_commit = run_command('git', 'rev-parse', '--short', 'HEAD', check:true).stdout().strip()
  endif
  if git_commit == ''
    version_number = '-Devel'
  else
    version_number = 'Git-@0@'.format(git_commit)
  endif
else
  name_suffix = ''
  version_number = meson.project_version()
endif

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('VERSION', version_number)
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)
conf.set('debug', get_option('debug'))
conf.set('app-name', 'Dev toolbox@0@'.format(name_suffix))

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
