# meson.build
# 
# Copyright (C) 2025 Alessandro Iepure
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()

# Configuration file
if get_option('debug')
  name_suffix = ' (Development)'
  
  git = find_program('git', required: false)
  if git.found()
    git_commit = run_command('git', 'rev-parse', '--short', 'HEAD', check:true).stdout().strip()
  endif

  if git_commit == ''
    version_str = meson.project_version() + '-dev'
  else
    version_str = meson.project_version() + '-dev (' + git_commit + ')'
  endif
else
  name_suffix = ''
  version_str = meson.project_version()
endif

conf = configuration_data()
conf.set_quoted('VERSION', version_str)
conf.set_quoted('GETTEXT_PACKAGE', 'devtoolbox')
conf.set_quoted('LOCALEDIR', get_option('prefix') / get_option('localedir'))
conf.set_quoted('PKGDATADIR', pkgdatadir)
conf.set_quoted('APP_NAME', 'Dev Toolbox@0@'.format(name_suffix))
conf.set_quoted('APP_ID', 'me.iepure.devtoolbox')

configure_file(
    input: 'config.rs.in',
    output: 'config.rs',
    configuration: conf
)

run_command(
  'cp',
  meson.project_build_root() / 'src' / 'config.rs',
  meson.project_source_root() / 'src' / 'config.rs',
  check: true
)

# Compile gresources
gnome = import('gnome')

blueprint_files = files(
  'core/ui/shortcuts-dialog.blp',
  'core/ui/window.blp',
  'core/ui/about-dialog.blp',

  'core/widgets/text_area/text_area.blp',
  'core/widgets/actionable_entryrow/actionable_entryrow.blp',

  'tools/cron_parser/specifier_row.blp',

  'tools/config_format/config_format.blp',
  'tools/timestamp/timestamp.blp',
  'tools/number_bases/number_bases.blp',
  'tools/cron_parser/cron_parser.blp',
  'tools/cron_gen/cron_gen.blp',
  'tools/linux_permissions/linux_permissions.blp',
  'tools/html_enc/html_enc.blp',
  'tools/base64/base64.blp',
  'tools/url_enc/url_enc.blp',
  'tools/lipsum/lipsum.blp',
  'tools/uuid/uuid.blp',
  'tools/random/random.blp',
  'tools/text_inspector/text_inspector.blp',
  'tools/contrast_check/contrast_check.blp',
  'tools/color_spaces/color_spaces.blp',
)

compile_blueprint = custom_target('blueprints',
  input: blueprint_files,
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('devtoolbox',
  'devtoolbox.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: compile_blueprint,
)

# Cargo build
cargo_bin  = find_program('cargo')
cargo_opt  = [ '--manifest-path', meson.project_source_root() / 'Cargo.toml' ]
cargo_opt += [ '--target-dir', meson.project_build_root()  / 'src' ]
cargo_env  = [ 'CARGO_HOME=' + meson.project_build_root()  / 'cargo-home' ]

if get_option('buildtype') == 'release'
  cargo_opt += [ '--release' ]
  rust_target = 'release'
else
  rust_target = 'debug'
endif

cargo_build = custom_target(
  'cargo-build',
  build_by_default: true,
  build_always_stale: true,
  output: meson.project_name(),
  console: true,
  install: true,
  install_dir: get_option('bindir'),
  command: [
    'env', cargo_env,
    cargo_bin, 'build',
    cargo_opt, '&&', 'cp', 'src' / rust_target / meson.project_name(), '@OUTPUT@',
  ]
)
