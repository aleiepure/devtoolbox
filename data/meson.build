# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

desktop_conf = configuration_data()
if get_option('debug')
  desktop_conf.set('app-name', 'Dev toolbox (Development snapshot)')
else
  desktop_conf.set('app-name', 'Dev toolbox')
endif
desktop_file = i18n.merge_file(
        input: configure_file(
		    output: 'me.iepure.devtoolbox.desktop.in',
		     input: 'me.iepure.devtoolbox.desktop.in.in',
	     configuration: desktop_conf
	),
       output: 'me.iepure.devtoolbox.desktop',
         type: 'desktop',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils, args: [desktop_file])
endif

appstream_file = i18n.merge_file(
        input: 'me.iepure.devtoolbox.appdata.xml.in',
       output: 'me.iepure.devtoolbox.appdata.xml',
       po_dir: '../po',
      install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util, args: ['validate', appstream_file])
endif

install_data('me.iepure.devtoolbox.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file',
       compile_schemas,
       args: ['--strict', '--dry-run', meson.current_source_dir()])
endif

subdir('icons')
