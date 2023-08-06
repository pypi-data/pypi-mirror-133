import os

from setuptools import setup


def read(relpath: str) -> str:
	with open(os.path.join(os.path.dirname(__file__), relpath)) as f:
		return f.read()


setup(
	name = 'aiodebug',
	version = read('version.txt').strip(),
	description = 'A tiny library for monitoring and testing asyncio programs',
	long_description = read('README.rst'),
	author = 'Quantlane',
	author_email = 'code@quantlane.com',
	url = 'https://gitlab.com/quantlane/libs/aiodebug',
	license = 'Apache 2.0',
	install_requires = [
		'typing-extensions>=3.7.0,<5.0.0',
	],
	extras_require = {
		'logwood': [
			'logwood>=3.0.0,<4.0.0'
		],
	},
	packages = [
		'aiodebug',
		'aiodebug.testing',
	],
	classifiers = [
		'License :: OSI Approved :: Apache Software License',
		'Natural Language :: English',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
	],
)
