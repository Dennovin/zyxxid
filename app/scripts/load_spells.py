#!/usr/bin/env python
import os
import sys

from zyxxid.spell import Spell

for key in Spell.bucket().get_keys():
    Spell.bucket().delete(key)

for fn in os.listdir(sys.argv[1]):
    Spell.load_from_file(os.path.join(sys.argv[1], fn)).store()
