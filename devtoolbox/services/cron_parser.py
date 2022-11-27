# Copyright (C) 2022 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

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