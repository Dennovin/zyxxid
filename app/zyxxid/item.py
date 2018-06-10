import docutils.core
import docutils.nodes
from docutils.writers import html4css1, latex2e

from . import database


class HTMLTranslator(html4css1.HTMLTranslator):
    def depart_document(self, node):
        super().depart_document(node)
        self.html_body.pop(0)
        self.html_body.pop()


class LaTeXTranslator(latex2e.LaTeXTranslator):
    pass


class Item(database.RiakStorable):
    _indexes = ["name"]

    @classmethod
    def load_from_file(cls, filename):
        item = cls()

        with open(filename) as fh:
            item.source = fh.read()
            doctree = docutils.core.publish_doctree(item.source)

            for attr in doctree.attributes["names"]:
                if attr.startswith("srd:"):
                    item._id = attr

            item.name = doctree[doctree.first_child_matching_class(docutils.nodes.title)].astext()

            paragraphs = []
            for paragraph in doctree.traverse(lambda x: isinstance(x, docutils.nodes.paragraph)):
                paragraphs.append(paragraph.astext().replace("\n", " "))

            item.plaintext = "\n".join(paragraphs)

            writer = html4css1.Writer()
            writer.translator_class = HTMLTranslator
            parts = docutils.core.publish_parts(item.source, writer=writer)
            item.html = parts["html_body"]

            writer = latex2e.Writer()
            writer.translator_class = LaTeXTranslator
            parts = docutils.core.publish_parts(item.source, writer=writer)
            item.latex = parts["body"]

        return item
