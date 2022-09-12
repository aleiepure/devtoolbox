# favorites_view.py
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

from gettext import gettext as _
from gi.repository import Gtk, Adw, Gio
from devtoolbox.service.json_formatter import JsonFormatter
from devtoolbox.service.sql_formatter import SqlFormatter
from devtoolbox.service.xml_formatter import XmlFormatter
from devtoolbox.views.utilities_view import UtilitiesView
from devtoolbox.widgets.base64_encoder_utility import Base64EncoderUtility
from devtoolbox.widgets.formatter_utility import FormatterUtility
from devtoolbox.widgets.gzip_encoder_utility import GZipEncoderUtility
from devtoolbox.widgets.hash_generator_utility import HashGeneratorUtility
from devtoolbox.widgets.html_encoder_utility import HtmlEncoderUtility
from devtoolbox.widgets.json2yaml_utility import Json2YamlUtility
from devtoolbox.widgets.jwt_decoder_utility import JWTDecoderUtility
from devtoolbox.widgets.lorem_ipsum_utility import LoremIpsumGenerator, LoremIpsumUtility
from devtoolbox.widgets.timestamp_utility import TimestampUtility
from devtoolbox.widgets.number_base_utility import NumberBaseUtility
from devtoolbox.widgets.cron_parser_utility import CronParserUtility
from devtoolbox.widgets.url_encoder_utility import UrlEncoderUtility


@Gtk.Template(resource_path="/me/iepure/devtoolbox/ui/empty_favorites.ui")
class EmptyFavorites(Adw.Bin):
    __gtype_name__ = "EmptyFavorites"

    def __init__(self):
        super().__init__()


class FavoritesView(Adw.Bin):

    view_stack = Adw.ViewStack(vexpand=True)

    settings = Gio.Settings(schema_id="me.iepure.devtoolbox")

    def __init__(self):
        super().__init__()

        self.empty_view = EmptyFavorites()
        self.filled_view = UtilitiesView(self.get_fav_utilities())

        self.view_stack.add_named(self.empty_view, "empty")
        self.view_stack.add_named(self.filled_view, "filled")

        fav_list = self.settings.get_strv("favorites")
        if len(fav_list) == 0:
            self.view_stack.set_visible_child_name("empty")
        else:
            self.view_stack.set_visible_child_name("filled")

        self.set_child(self.view_stack)
        self.settings.connect("changed", self.on_settings_change)

    def on_settings_change(self, key, data):
        fav_list = self.settings.get_strv("favorites")
        if len(fav_list) == 0:
            self.view_stack.set_visible_child_name("empty")
        else:
            self.view_stack.remove(self.filled_view)
            self.filled_view = UtilitiesView(self.get_fav_utilities())
            self.view_stack.add_named(self.filled_view, "filled")
            self.view_stack.set_visible_child_name("filled")

    def get_fav_utilities(self):
        UTILITIES = {
            "json2yaml": {
                "title": _("JSON - YAML"),
                "icon-name": "right-left-symbolic",
                "child": Json2YamlUtility()
            },
            "timestamp": {
                "title": _("Timestamp"),
                "icon-name": "clock-rotate-symbolic",
                "child": TimestampUtility()
            },
            "baseconverter": {
                "title": _("Number Base"),
                "icon-name": "hashtag-symbolic",
                "child": NumberBaseUtility()
            },
            "cronparser": {
                "title": _("Cron Parser"),
                "icon-name": "hourglass-half-symbolic",
                "child": CronParserUtility()
            },
            "htmlencoder": {
                "title": _("HTML"),
                "icon-name": "code-symbolic",
                "child": HtmlEncoderUtility()
            },
            "urlencoder": {
                "title": _("URL"),
                "icon-name": "link-symbolic",
                "child": UrlEncoderUtility()
            },
            "base64encoder": {
                "title": _("Base64"),
                "icon-name": "base64-symbolic",
                "child": Base64EncoderUtility()
            },
            "gzipencoder": {
                "title": _("GZip"),
                "icon-name": "file-zip-symbolic",
                "child": GZipEncoderUtility()
            },
            "jwtdecoder": {
                "title": _("JWT"),
                "icon-name": "key-symbolic",
                "child": JWTDecoderUtility()
            },
            "jsonformatter": {
                "title": "JSON",
                "icon-name": "right-left-symbolic",
                "child": FormatterUtility(JsonFormatter())
            },
            "sqlformatter": {
                "title": "SQL",
                "icon-name": "clock-rotate-symbolic",
                "child": FormatterUtility(SqlFormatter())
            },
            "xmlformatter": {
                "title": "XML",
                "icon-name": "hashtag-symbolic",
                "child": FormatterUtility(XmlFormatter())
            },
            "hashgen": {
                "title": "Hash generator",
                "icon-name": "hashtag-symbolic",
                "child": HashGeneratorUtility()
            },
            "loremipsum": {
                "title": "Lorem Ipsum",
                "icon-name": "paragraph-symbolic",
                "child": LoremIpsumUtility()
            }
        }

        fav_str_list = self.settings.get_strv("favorites")
        fav_obj_dict = {title:UTILITIES[title] for title in fav_str_list}
        return fav_obj_dict
