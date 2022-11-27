# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

# scalable_dir = join_paths('hicolor', 'scalable', 'apps')
# install_data(
#   join_paths(scalable_dir, ('@0@.svg').format(application_id)),
#   install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
# )

# symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
# install_data(
#   join_paths(symbolic_dir, ('@0@-symbolic.svg').format(application_id)),
#   install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
# )

# Installing the default icon
install_data(
    join_paths('hicolor/scalable/apps', project_id + '.svg'),
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'icons/hicolor/scalable/apps')
)

# Installing the symbolic icon
install_data(
    join_paths('hicolor/symbolic/apps', project_rdnn_name + '-symbolic.svg'),
    install_dir: join_paths(get_option('prefix'), get_option('datadir'), 'icons/hicolor/symbolic/apps'),
    rename: '@0@-symbolic.svg'.format(project_id)
)
