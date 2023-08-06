from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
	name="milwaukee_dpw_parser",
	packages=["milwaukee_dpw_parser"],
	version="0.1.1",
	description="Milwaukee Wisconsin Department of Public Works Parser",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/jasonfry89/milwaukee-dpw-parser",
	license="MIT",
	keywords=[
		"Milwaukee", 
		"Wisconsin", 
		"Garbage", 
		"Recycling", 
		"DPW",
	],
	author="Jason Fry",
	python_requires=">=3",
	setup_requires=[
		"wheel",
	],
	install_requires=[
		"beautifulsoup4>=4.6.1",
		"aiohttp>=3.6.0",
	],
)        
