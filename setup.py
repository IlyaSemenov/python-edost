from distutils.core import setup

"""
Python bindings for edost.ru, a Russian delivery cost calculation service.
"""

setup(
	name='edost',
	version='0.1',
	url='https://github.com/IlyaSemenov/python-edost',
	license='BSD',
	author='Ilya Semenov',
	author_email='ilya@semenov.co',
	description='Python bindings for edost.ru',
	long_description=__doc__,
	packages=['edost'],
)
