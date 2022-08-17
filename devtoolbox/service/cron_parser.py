# cron_parser.py
#
# Copyright 2022 Alessandro Iepure
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from crontab import CronTab, CronSlices
from dateutil import parser
from datetime import datetime


class CronParser():

    @staticmethod
    def is_expression_valid(expression):
        return CronSlices.is_valid(expression)

    @staticmethod
    def is_date_format_valid(format):
        try:
            parser.parse(datetime.now().strftime(format))
            return True
        except parser._parser.ParserError:
            return False

    @staticmethod
    def generate_dates(expression="*", format="%c", number=5):
        cron = CronTab()
        job = cron.new(command='/usr/bin/echo')
        job.setall(expression)
        schedule = job.schedule()
        string = ""
        for _ in range(0, number):
            string += schedule.get_next().strftime(format) + "\n"
        return string