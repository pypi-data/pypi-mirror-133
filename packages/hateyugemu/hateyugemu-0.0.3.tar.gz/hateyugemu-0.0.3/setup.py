import setuptools

with open('README.md', 'r', encoding = 'utf-8') as fh:
	long_description = fh.read()

setuptools.setup(
	name = "hateyugemu",
	version = "0.0.3",
	author = "Kai Wang",
	license = "MIT",
	description = "A board game.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/kaiwinut/hateyugemu",
	project_urls = {
		"Bug Reports": "https://github.com/kaiwinut/hateyugemu/issues",
		"Source Code": "https://github.com/kaiwinut/hateyugemu",
	},
	classifiers = [
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3 :: Only",
		"Programming Language :: Python :: 3.7",
		"Programming Language :: Python :: 3.8",
		"Programming Language :: Python :: 3.9",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	packages = setuptools.find_packages(where = "src"),
	package_dir = {"": "src"},
	include_package_data = True,
	package_data = {'hateyugemu': ['data/*.txt', 'data/*.csv']},
	python_requires = ">=3.7",
)