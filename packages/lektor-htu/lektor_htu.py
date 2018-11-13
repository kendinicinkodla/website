# -*- coding: utf-8 -*-
from io import StringIO

from jinja2.filters import do_indent
from lektor.pluginsystem import Plugin, get_plugin
from lxml import etree
from lxml.html import Classes
from lxml.html.defs import empty_tags
from markupsafe import Markup

import vkbeautify


def tweak_html(text, docutils=None, section=None, col=None, th=None, container=None):
    root = etree.HTML(text.html)
    if root is None:
        return text

    body = root.xpath("/html/body")[0]

    config = get_plugin("htu").get_config()
    tweaks = config.section_as_dict("tweaks")
    docutils = config.section_as_dict("docutils")

    # convert divs with section class into section elements
    section = section if section is not None else docutils.get("section", False)
    if section:
        for node in body.cssselect("div.section"):
            node.tag = "section"

    # remove colgroups and their cols from table elements
    col = col if col is not None else docutils.get("col", False)
    if col:
        for node in body.xpath("//colgroup"):
            node.getparent().remove(node)

    # remove head class from th elements
    th = th if th is not None else docutils.get("th", False)
    if th:
        for node in body.cssselect("th.head"):
            classes = Classes(node.attrib)
            classes.discard("head")

    # remove docutils generated container class attributes
    container = container if container is not None else docutils.get("container", False)
    if container:
        for node in body.xpath('//*[contains(@class, "docutils container")]'):
            classes = Classes(node.attrib)
            classes.discard("container")
            classes.discard("docutils")

    # remove docutils generated docutils class attributes
    docutils = docutils if docutils is not None else docutils.get("docutils", False)
    if docutils:
        for node in body.cssselect(".docutils"):
            classes = Classes(node.attrib)
            classes.discard("docutils")

    # produce new output
    output_format = tweaks.get("format", "html")
    if output_format == "xml":
        for node in body.iter():
            if (node.text is None) and (node.tag not in empty_tags):
                node.text = ""

    cleaned = StringIO()
    for child in body:
        child_html = etree.tostring(
            child, encoding="unicode", method=output_format, pretty_print=True
        )
        cleaned.write(child_html)

    content = cleaned.getvalue()
    if (output_format == "xml") and (tweaks.get("pretty_print", False)):
        indent = tweaks.get("indent", "\t")
        content = vkbeautify.xml(content, indent=indent)

    return Markup(content)


def indent_html(text, indents=0):
    if indents == 0:
        return text
    try:
        content = text.html
    except AttributeError:
        content = str(text)
    if len(content.strip()) == 0:
        return text
    return Markup(do_indent(content, width=indents))


class HTUPlugin(Plugin):
    name = "htu"
    description = "Personal tweaks for HTML output"

    def on_setup_env(self, **extra):
        self.env.jinja_env.filters["htu"] = tweak_html
        self.env.jinja_env.filters["indent_by"] = indent_html
