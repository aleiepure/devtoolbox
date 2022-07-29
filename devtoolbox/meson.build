pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'devtoolbox')

subdir('views')
subdir('widgets')

sources = [
  '__init__.py',
  'application.py',
  'window.py',
  'params.py'
]

install_data(sources, install_dir: moduledir)