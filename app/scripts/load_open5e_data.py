#!/usr/bin/env python
from docutils.parsers.rst import roles
import docutils.nodes
import os
import pickle
import sys

from zyxxid.item import Item

open5e_dir = sys.argv[1]
item_dir = os.path.join(open5e_dir, "source", "equipment", "magic-items")

doc_titles = {}

for root, dirs, files in os.walk(open5e_dir):
    for fn in files:
        if fn.endswith(".doctree"):
            with open(os.path.join(root, fn), "rb") as fh:
                doc = pickle.load(fh)

                titles = doc.traverse(lambda x: isinstance(x, docutils.nodes.title))
                doc_title = titles[0].astext()

                section = doc.traverse(lambda x: isinstance(x, docutils.nodes.section))[0]
                for nameattr in section.attributes["names"]:
                    if nameattr.startswith("srd:"):
                        doc_titles[nameattr] = doc_title

def reference_role(role, rawtext, text, lineno, inliner, options={}, content=[]):
    text = doc_titles.get(text, text)
    node = docutils.nodes.emphasis(rawtext, text)
    return [node], []

roles.register_local_role("ref", reference_role)

for fn in os.listdir(item_dir):
    if fn.endswith(".rst") and fn != "index.rst":
        item = Item.load_from_file(os.path.join(item_dir, fn))
        item.store()

        print("Loaded item: {}".format(item.name))
