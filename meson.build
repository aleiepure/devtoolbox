project(
  'devtoolbox',  
  version: '0.1.0',
  meson_version: '>= 0.50.0',
  license: 'GPL-3.0-or-later'
)

# Module imports
python = import('python')
gnome = import('gnome')
i18n = import('i18n')

# NAME_SUFFIX is used in the about dialog
if get_option('profile') == 'development'
  PROFILE = '.Devel'
  NAME_SUFFIX = ' (Development)'
else
  PROFILE = ''
  NAME_SUFFIX = ''
endif

# Constants
project_id = 'me.iepure.devtoolbox'.format(PROFILE)
project_rdnn_name = 'me.iepure.devtoolbox'

# Python installed and found
message('Looking for python3...')
py_installation = python.find_installation('python3')
if not py_installation.found()
    error('No valid python3 binary found')
else
    message('Found python3 binary')
endif

# Dependencies
message('Looking for dependencies...')
dependency('gtk4', version: '>=4.3.1')
dependency('libadwaita-1', version: '>=1.2')
dependency('gtksourceview-5', version: '>=5.6')

# Paths
python_dir = join_paths(get_option('prefix'), py_installation.get_install_dir())
data_dir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
bindir = join_paths(get_option('prefix'), get_option('bindir'))

# Install binary executable
conf = configuration_data()
conf.set('DATA_DIR', data_dir)
conf.set('PYTHON_DIR', python_dir)
conf.set('VERSION', meson.project_version())
conf.set('APPID', project_id)
conf.set('PYTHON', python.find_installation('python3').path())
conf.set('LOCALE_DIR', join_paths(get_option('prefix'), get_option('localedir')))


install_subdir(
  'devtoolbox',
  install_dir: python_dir
)

message('Preparing bin file')
configure_file(
  input: 'devtoolbox.in',
  output: 'devtoolbox',
  configuration: conf,
  install_dir: bindir,
)

subdir('data')
subdir('po')


gnome.post_install(
    glib_compile_schemas: true,
    gtk_update_icon_cache: true,
    update_desktop_database: true
)

#meson.add_install_script('meson/postinstall.py')