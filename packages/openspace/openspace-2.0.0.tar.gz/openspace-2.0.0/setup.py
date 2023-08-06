#!/usr/bin/env python

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name="openspace",
	version="2.0.0",
	python_requires='>3.8.0',
	description="Public package for various space operations applications",
	long_description=long_description,
	author="Brandon Sexton",
	author_email="brandon.sexton.1@outlook.com",
	entry_points={'console_scripts': [
        'openspace=openspace.examples.geoplanner:run',
	    'reach_demo=openspace.examples.reach_demo:run',
	    'joystick=openspace.examples.joystick:run',
	    'sda_demo=openspace.examples.sda_demo:run']},
	packages=find_packages(),
	include_package_data=True,
	install_requires=[]
	)
