pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
viewsdir = join_paths(pkgdatadir, 'devtoolbox/views')

sources = [
  '__init__.py',
  'tab_content.py',
  'favorites.py',
]

install_data(sources, install_dir: viewsdir)