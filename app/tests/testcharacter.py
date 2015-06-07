#!/usr/bin/env python
import nose
import os
import sys

testdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(testdir, os.pardir))

import Incarnate

def test_character_pdf():
    character = Incarnate.Character.load_from_file(os.path.join(testdir, "testcharacter.yaml"))
    Incarnate.PDF.write_pdf(character)
