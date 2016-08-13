#!/usr/bin/env python
import argparse
import os
import sys

from zyxxid.character import Template, TemplateFile

parser = argparse.ArgumentParser(description="Load a character sheet template.")
parser.add_argument("name", help="Template identifier, no spaces.")
parser.add_argument("display_name", help="Template name, for display.")
parser.add_argument("description", help="Template description.")
parser.add_argument("files", metavar="N", nargs="+",
                    help="File(s) needed by the template.")
args = parser.parse_args()

template = Template()
template.name = args.name
template.display_name = args.display_name
template.description = args.description
template.files = []

for fn in args.files:
    template_file = TemplateFile.store_from_file(fn)
    template.files.append({"id": template_file._id, "filename": os.path.basename(fn)})

template.store()
