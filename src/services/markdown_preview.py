# Copyright (C) 2022 - 2023 Alessandro Iepure
#
# SPDX-License-Identifier: GPL-3.0-or-later

from gi.repository import Gio, GObject, Adw
import markdown2


class MarkdownPreviewService():

    def __init__(self):
        self._cancellable = Gio.Cancellable()
        self._html_file = Gio.File.new_tmp("me.iepure.devtoolbox.XXXXXX")[0]

    def set_markdown(self, markdown:str):
        self._markdown = markdown

    def get_cancellable(self) -> Gio.Cancellable:
        return self._cancellable

    def async_finish(self, result:Gio.AsyncResult, caller:GObject.Object):
        if not Gio.Task.is_valid(result, caller):
            return -1
        self._markdown = None
        return result.propagate_value().value

    def get_html_file_path(self):
        return self._html_file.get_path()

    def build_html_from_markdown_async(self, caller:GObject.Object, callback:callable):
        task = Gio.Task.new(caller, None, callback, self._cancellable)
        task.set_return_on_cancel(True)
        task.run_in_thread(self.build_html_from_markdown_thread)

    def build_html_from_markdown_thread(self, task:Gio.Task, source_object:GObject.Object, task_data:object, cancelable:Gio.Cancellable):
        if task.return_error_if_cancelled():
            return
        outcome = self.build_html_from_markdown(self._markdown)
        task.return_value(outcome)

    def build_html_from_markdown(self, markdown_str:str):

        self._markdown_css = ""
        self._code_colors = ""
        self._scrollpos_script = ""

        if not self._markdown_css:
            gfile = Gio.File.new_for_uri("resource:///me/iepure/devtoolbox/markdown-preview/github-markdown.css")
            self._markdown_css = gfile.load_contents(None)[1].decode("utf-8")

        if not self._code_colors:
            if Adw.StyleManager.get_default().get_dark():
                gfile = Gio.File.new_for_uri("resource:///me/iepure/devtoolbox/markdown-preview/fenced-code-colors-dark.css")
            else:
                gfile = Gio.File.new_for_uri("resource:///me/iepure/devtoolbox/markdown-preview/fenced-code-colors-light.css")
            
            self._code_colors = gfile.load_contents(None)[1].decode("utf-8")

        if not self._scrollpos_script:
            gfile = Gio.File.new_for_uri("resource:///me/iepure/devtoolbox/markdown-preview/scrollpos-script.js")
            self._scrollpos_script = gfile.load_contents(None)[1].decode("utf-8")

        output = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <style>
"""
        output += self._markdown_css
        output += self._code_colors
        output += """</style>
<script>
"""
        output += self._scrollpos_script
        output += """</script>
</head>
<body class="markdown-body">
"""
        output += markdown2.markdown(markdown_str, extras=["tables", "fenced-code-blocks", "header-ids", "smarty-pants", "cuddled-lists", "strike"])
        output += """</body>
</html>
"""

        with open(self._html_file.get_path(), "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
            output_file.write(output)

        return self._html_file.get_path()
