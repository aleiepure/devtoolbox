# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

application_id = 'me.iepure.devtoolbox'

if get_option('debug') == true
  scalable_dir = join_paths('hicolor', 'scalable', 'apps')
  install_data(
  	join_paths(scalable_dir, ('@0@.Devel.svg').format(application_id)),
  	install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir),
  	rename: [('@0@.svg').format(application_id)]
	)
else
	scalable_dir = join_paths('hicolor', 'scalable', 'apps')
	install_data(
		join_paths(scalable_dir, ('@0@.svg').format(application_id)),
		install_dir: join_paths(get_option('datadir'), 'icons', scalable_dir)
	)
endif

symbolic_dir = join_paths('hicolor', 'symbolic', 'apps')
install_data(
  join_paths(symbolic_dir, ('@0@-symbolic.svg').format(application_id)),
  install_dir: join_paths(get_option('datadir'), 'icons', symbolic_dir)
)
