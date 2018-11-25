from __future__ import unicode_literals

import re
from datetime import datetime
from io import StringIO
from weakref import ref as weakref

import docutils
from bs4 import BeautifulSoup
from docutils.core import Publisher
from docutils.writers import get_writer_class
from lektor.context import get_ctx
from lektor.pluginsystem import Plugin, get_plugin
from lektor.types import Type
from markupsafe import Markup
from tidylib import tidy_fragment


_TRUE = {True, "yes"}

_re_dashes = re.compile(r"^(\s*)(---*)", re.MULTILINE)
_re_sc_end = re.compile(r"\s+\/\>")


def clean_html(text, **options):
    def remove_class(n, c):
        cs = n.attrs["class"]
        cs.remove(c)
        if len(cs) == 0:
            del n.attrs["class"]

    if len(text.strip()) == 0:
        return text

    soup = BeautifulSoup(text, "html.parser")

    config = get_plugin("rst").get_config()
    clean_options = config.section_as_dict("clean")

    # convert divs with section class into section elements
    if clean_options.get("div_to_section", True) in _TRUE:
        for node in soup.find_all("div", class_="section"):
            node.name = "section"

    # remove colgroups and their cols from table elements
    if clean_options.get("remove_colgroup", True) in _TRUE:
        for node in soup.find_all("colgroup"):
            node.decompose()

    # remove head class from th elements
    if clean_options.get("remove_th_head_class", True) in _TRUE:
        for node in soup.find_all("th", class_="head"):
            remove_class(node, "head")

    # remove docutils generated container class attributes
    if clean_options.get("remove_docutils_container_class", True) in _TRUE:
        for node in soup.select('div[class*="docutils container"]'):
            remove_class(node, "container")

    # remove docutils generated docutils class attributes
    if clean_options.get("remove_docutils_class", True) in _TRUE:
        for node in soup.find_all(class_="docutils"):
            remove_class(node, "docutils")

    text = str(soup)

    tidy_options = config.section_as_dict("tidy")
    tidy_enabled = tidy_options.pop("enabled", False)
    remove_sc_slash = tidy_options.pop("remove_space_before_self_closing_slash", False) in _TRUE
    if tidy_enabled in _TRUE:
        text, errors = tidy_fragment(text, options=tidy_options)
        if (tidy_options.get("output-xhtml", False) in _TRUE) and remove_sc_slash:
            text = _re_sc_end.sub("/>", text)

    return text


def rst_to_html(text, extra_params, record, clean=True):
    ctx = get_ctx()
    if ctx is None:
        raise RuntimeError("Context is required for rendering")

    text = _re_dashes.sub(r"\1-\2", text)

    try:
        plugin = get_plugin("rst")
        config = plugin.get_config()
        settings = config.section_as_dict("docutils")
        writer_name = settings.pop("writer", "html")
        extra_params.update(settings)
    except:
        writer_name = "html"

    Writer = get_writer_class(writer_name)
    pub = Publisher(destination_class=docutils.io.StringOutput, writer=Writer())
    pub.set_components("standalone", "restructuredtext", "html")
    pub.process_programmatic_settings(None, extra_params, None)
    pub.set_source(
        source=StringIO(text),
        source_path=record.source_filename if record is not None else None,
    )
    pub.publish()

    metadata = {}
    for docinfo in pub.document.traverse(docutils.nodes.docinfo):
        for element in docinfo.children:
            if element.tagname == "field":
                name_elem, body_elem = element.children
                name = name_elem.astext()
                value = body_elem.astext()
            else:
                name = element.tagname
                value = element.astext()
            name = name.lower()
            if name == "date":
                value = datetime.strptime(value, "%Y-%m-%d %H:%M")
            metadata[name] = value

    parts = pub.writer.parts
    body = parts["html_title"] + parts["html_subtitle"] + parts["fragment"]

    if clean:
        body = clean_html(body)

    return body, metadata


class Rst(object):
    def __init__(self, source, extra_params, record):
        self.source = source
        self.extra_params = extra_params
        self.__record = weakref(record) if record is not None else lambda: None
        self.__cached_for_ctx = None
        self.__html = None
        self.__meta = None

    def __bool__(self):
        return bool(self.source)

    def __nonzero__(self):
        return bool(self.source)

    def __render(self):
        # When the markdown instance is attached to a cached object we can
        # end up in the situation where the context changed from the time
        # we were put into the cache to the time where we got referenced
        # by something elsewhere.  In that case we need to re-process our
        # markdown.  For instance this affects relative links.
        if self.__html is None or self.__cached_for_ctx != get_ctx():
            self.__html, self.__meta = rst_to_html(
                self.source, self.extra_params, self.__record()
            )
            self.__cached_for_ctx = get_ctx()

    @property
    def meta(self):
        self.__render()
        return self.__meta

    @property
    def html(self):
        self.__render()
        return Markup(self.__html)

    def __getitem__(self, name):
        return self.meta[name]

    def __unicode__(self):
        self.__render()
        return self.__html

    def __html__(self):
        self.__render()
        return Markup(self.__html)


class RstDescriptor(object):
    def __init__(self, source, extra_params):
        self.source = source
        self.extra_params = extra_params

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return Rst(self.source, self.extra_params, obj)


class RstType(Type):
    widget = "multiline-text"

    def __init__(self, env, options):
        Type.__init__(self, env, options)
        self.extra_params = {
            "doctitle_xform": False,
            "initial_header_level": "2",
            "syntax_highlight": "short",
        }
        self.extra_params.update(options)

    def value_from_raw(self, raw):
        return RstDescriptor(raw.value or "", self.extra_params)


class RstPlugin(Plugin):
    name = "reStructuredText"
    description = "Adds reStructuredText support"

    def on_setup_env(self, **extra):
        self.env.types["rst"] = RstType
