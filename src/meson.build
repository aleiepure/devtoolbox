# meson.build
#
# Copyright (C) 2022-2025 Alessandro Iepure
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
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
conf.set_quoted('APP_ID', 'me.iepure.Devtoolbox')

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

# Handle subdirectories
subdir('core')
subdir('tools')

# Compile gresources
gnome = import('gnome')

blueprint_files = files(
  'core/ui/shortcuts-dialog.blp',
  'core/ui/window.blp',
  'core/ui/about-dialog.blp',

  'core/widgets/tool_title/tool_title.blp',
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
