# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

desktop_conf = configuration_data()
if get_option('debug')
  desktop_conf.set('app-name', 'Dev Toolbox (Development snapshot)')
else
  desktop_conf.set('app-name', 'Dev Toolbox')
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
        input: 'me.iepure.devtoolbox.metainfo.xml.in',
       output: 'me.iepure.devtoolbox.metainfo.xml',
       po_dir: '../po',
      install: true,
  install_dir: get_option('datadir') / 'metainfo'
)

appstreamcli = find_program('appstreamcli', required: false, disabler: true)
test('Validate appstream file', appstreamcli,
     args: ['validate', '--no-net', '--explain', appstream_file])

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
