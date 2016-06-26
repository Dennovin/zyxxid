#!/usr/bin/env python
import nose
import os
import requests
import sys

from zyxxid.character import Character, PDF

testdir = os.path.dirname(os.path.abspath(__file__))

def test_character_pdf():
    character = Character.load_from_file(os.path.join(testdir, "testcharacter.yaml"))
    character.store()

    req = requests.post("http://localhost/pdf", data={"character_id": character.id})
