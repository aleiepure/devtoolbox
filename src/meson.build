# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'devtoolbox')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'ui/gtk/help-overlay.blp',
    'ui/views/json_yaml.blp',
    'ui/views/jwt_decoder.blp',
    'ui/views/markdown_preview.blp',
    'ui/views/regex_tester.blp',
    'ui/views/text_diff.blp',
    'ui/views/xml_validator.blp',
    'ui/views/cron_converter.blp',
    'ui/views/formatter.blp',
    'ui/views/base64_encoder.blp',
    'ui/views/html_encoder.blp',
    'ui/views/url_encoder.blp',
    'ui/views/gzip_compressor.blp',
    'ui/views/contrast_checker.blp',
    'ui/views/color_converter.blp',
    'ui/views/base_converter.blp',
    'ui/views/certificate_parser.blp',
    'ui/views/random_generator.blp',
    'ui/views/timestamp.blp',
    'ui/views/certificate_request_generator.blp',
    'ui/views/reverse_cron.blp',
    'ui/views/chmod_calculator.blp',
    'ui/views/hash_generator.blp',
    'ui/views/image_converter.blp',
    'ui/views/lorem_generator.blp',
    'ui/views/text_inspector.blp',
    'ui/views/uuid_generator.blp',
    'ui/views/colorblindness_simulator.blp',
    'ui/views/qrcode_generator.blp',
    'ui/views/json_validator.blp',
    'ui/widgets/date_area.blp',
    'ui/widgets/file_view.blp',
    'ui/widgets/text_area.blp',
    'ui/widgets/utility_title.blp',
    'ui/widgets/image_area.blp',
    'ui/widgets/text_file_area.blp',
    'ui/widgets/webview_area.blp',
    'ui/widgets/entry_row.blp',
    'ui/widgets/theme_switcher.blp',
    'ui/widgets/spin_area.blp',
    'ui/about_dialog.blp',
    'ui/window.blp'
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('devtoolbox',
  'devtoolbox.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
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
conf.set('app-name', 'Dev Toolbox@0@'.format(name_suffix))

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
subdir('formatters')

devtoolbox_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'utils.py',
]

install_data(devtoolbox_sources, install_dir: moduledir)
