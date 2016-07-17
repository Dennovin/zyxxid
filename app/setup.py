import os
from datetime import datetime
from setuptools import setup, find_packages

setup(
    name="zyxxid",
    description="zyxxid.xyz",
    version="{0:%Y%m%d}.{0:%H%M%S}".format(datetime.utcnow()),
    author="Corey Cossentino",
    author_email="corey@cossentino.com",
    packages=find_packages(),
    package_data={
        "zyxxid": ["templates/*.j2"],
    },
    package_dir={
        "zyxxid": "zyxxid",
    },
    install_requires=[
        "flask",
        "riak",
        "PyYAML",
        "uWSGI",
        "celery",
        "Jinja2",
        "requests",
        "pylibmc",
        "simplejson",
        "google-api-python-client",
        ],
#    scripts=["scripts/{}".format(i) for i in os.listdir("scripts")],
    )
