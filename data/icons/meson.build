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

application_id = 'me.iepure.Devtoolbox'
scalable_dir = 'hicolor' / 'scalable' / 'apps'

if get_option('debug') == true
  install_data(
    scalable_dir / ('@0@.Devel.svg').format(application_id),
  	install_dir: get_option('datadir') / 'icons' / scalable_dir,
  	rename: [('@0@.svg').format(application_id)]
	)
else
	install_data(
		scalable_dir / ('@0@.svg').format(application_id),
		install_dir: get_option('datadir') / 'icons' / scalable_dir
	)
endif

symbolic_dir = 'hicolor' / 'symbolic' / 'apps'
install_data(
  symbolic_dir / ('@0@-symbolic.svg').format(application_id),
  install_dir: get_option('datadir') / 'icons' / symbolic_dir
)
