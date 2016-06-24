#!/usr/bin/env python
import nose
import os
import sys

testdir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(testdir, os.pardir))

import zyxxid.character

def test_celery_task():
    character = zyxxid.character.Character.load_from_file(os.path.join(testdir, "testcharacter.yaml"))
    zyxxid.character.create_pdf.delay(character)

