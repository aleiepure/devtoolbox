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

# Desktop file
conf = configuration_data()
if get_option('debug')
  conf.set('app-name', 'Dev Toolbox (Development)')
else
  conf.set('app-name', 'Dev Toolbox')
endif

desktop_config = configure_file(
  output: 'me.iepure.Devtoolbox.desktop.in',
  input: 'me.iepure.Devtoolbox.desktop.in.in',
  configuration: conf,
)

desktop_file = i18n.merge_file(
  input: desktop_config,
  output: 'me.iepure.Devtoolbox.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: get_option('datadir') / 'applications'
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

# AppStream metainfo file
appstream_file = i18n.merge_file(
        input: 'me.iepure.Devtoolbox.metainfo.xml.in',
       output: 'me.iepure.Devtoolbox.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

# GSchema
install_data('me.iepure.Devtoolbox.gschema.xml',
  rename: '@0@.gschema.xml'.format('me.iepure.Devtoolbox'),
  install_dir: get_option('datadir') / 'glib-2.0' / 'schemas',
)

compile_schemas = find_program('glib-compile-schemas', required: false, disabler: true)
test('Validate schema file',
     compile_schemas,
     args: ['--strict', '--dry-run', meson.current_source_dir()])

# Search provider (Service)
# configure_file(
#   input: 'me.iepure.Devtoolbox.SearchProvider.service.in',
#   output: 'me.iepure.Devtoolbox.SearchProvider.service',
#   configuration: configuration_data({
#     'bindir': get_option('prefix') / get_option('bindir')
#   }),
#   install: true,
#   install_dir: get_option('datadir') / 'dbus-1' / 'services'
# )

# install_data('me.iepure.Devtoolbox.SearchProvider.ini',
#   install_dir: get_option('datadir') / 'gnome-shell' / 'search-providers'
# )

# Subdirectories
subdir('icons')
