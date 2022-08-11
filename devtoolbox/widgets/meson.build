pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
widgetsdir = join_paths(pkgdatadir, 'devtoolbox/widgets')

sources = [
  '__init__.py',
  'sidebar_element.py',
  'json2yaml_utility.py',
  'timestamp_utility.py',
  'number_base_utility.py',
  'cron_parser_utility.py',
  'html_encode_utility.py',
  'url_encoder_utility.py',
  'base64_utility.py'
]

install_data(sources, install_dir: widgetsdir)