# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())

gnome.compile_resources('devtoolbox',
  'devtoolbox.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

# Merging the translations with the desktop file
desktop_conf = configuration_data()
desktop_conf.set('icon', project_id)
i18n.merge_file(
  type: 'desktop',
  input: configure_file(
    output: project_rdnn_name + '.desktop.in',
    input: project_rdnn_name + '.desktop.in.in',
    configuration: desktop_conf),
  output: project_id + '.desktop',
  po_dir: join_paths(meson.project_source_root(), 'po'),
  install: true,
  install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'applications')
)

# Validating the desktop file
desktop_file_validate = find_program('desktop-file-validate', required:false)
if desktop_file_validate.found()
  test (
    'Validate desktop file',
    desktop_file_validate,
    args: join_paths(meson.current_build_dir (), project_id + '.desktop')
  )
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
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('me.iepure.devtoolbox.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
else
  message('not found')
endif

subdir('icons')