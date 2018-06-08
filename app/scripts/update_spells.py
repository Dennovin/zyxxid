#!/usr/bin/env python
import os
import sys

from zyxxid.spell import Spell

for fn in os.listdir(sys.argv[1]):
    spell = Spell.load_from_file(os.path.join(sys.argv[1], fn))
    existing = Spell.query("title", spell.title)

    if len(existing) == 0:
        spell.store()
