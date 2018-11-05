# -*- coding: utf-8 -*-
from io import StringIO

from lektor.pluginsystem import Plugin
from lxml import etree
from markupsafe import Markup


def tweak_html(text):
    root = etree.HTML(text.html)
    if root is None:
        return text

    body = root.xpath("/html/body")[0]

    # convert divs with section class into section elements
    for node in body.xpath('//div[@class="section"]'):
        node.tag = "section"

    # remove colgroup elements and their col children
    for node in body.xpath("//table/colgroup"):
        node.getparent().remove(node)

    # remove head class from th elements
    for node in body.xpath('//th[@class="head"]'):
        del node.attrib["class"]

    # produce new output
    cleaned = StringIO()
    for child in body:
        child_html = etree.tostring(
            child, encoding="unicode", method="html", pretty_print=True
        )
        cleaned.write(child_html)
    return Markup(cleaned.getvalue())


class HTUPlugin(Plugin):
    name = "htu"
    description = "Personal tweaks for HTML output"

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters["htu"] = tweak_html
