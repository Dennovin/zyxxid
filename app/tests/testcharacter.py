#!/usr/bin/env python
import nose
import os
import sys

from zyxxid.character import Character, PDF

testdir = os.path.dirname(os.path.abspath(__file__))

def test_character_pdf():
    character = Character.load_from_file(os.path.join(testdir, "testcharacter.yaml"))
    PDF.create(character)
