# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# standard imports
from datetime import datetime


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))  # the directory of this file
source_dir = os.path.dirname(script_dir)  # the source folder directory
root_dir = os.path.dirname(source_dir)  # the root folder directory

try:
    sys.path.insert(0, root_dir)
    from pyra import definitions  # put this in a try/except to prevent flake8 warning
except Exception:
    sys.exit(1)

# -- Project information -----------------------------------------------------
project = definitions.Names().name
project_copyright = f'{datetime.now ().year}, {project}'
author = 'ReenigneArcher'

# The full version, including alpha/beta/rc tags
# https://docs.readthedocs.io/en/stable/reference/environment-variables.html#envvar-READTHEDOCS_VERSION
version = os.getenv('READTHEDOCS_VERSION', 'dirty')


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'm2r2',  # enable markdown files
    'numpydoc',  # this automatically loads `sphinx.ext.autosummary` as well
    'sphinx.ext.autodoc',  # autodocument modules
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.todo',  # enable to-do sections
    'sphinx.ext.viewcode'  # add links to view source code
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['toc.rst']

# Extensions to include.
source_suffix = ['.rst', '.md']


# -- Options for HTML output -------------------------------------------------

# images
html_favicon = os.path.join(definitions.Paths().ROOT_DIR, 'web', 'images', 'retroarcher.ico')
html_logo = os.path.join(definitions.Paths().ROOT_DIR, 'web', 'images', 'logo-circle.png')

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# These paths are either relative to html_static_path
# or fully qualified paths (eg. https://...)
# html_css_files = [
#     'css/custom.css',
# ]
# html_js_files = [
#     'js/custom.js',
# ]

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'furo'

html_theme_options = {
    "top_of_page_button": "edit",
    "source_edit_link": "https://github.com/lizardbyte/retroarcher/blob/master/docs/source/{filename}",
}

# extension config options
autodoc_preserve_defaults = True  # Do not evaluate default arguments of functions
autosectionlabel_prefix_document = True  # Make sure the target is unique
todo_include_todos = True

# numpydoc config
numpydoc_validation_checks = {'all', 'SA01'}  # Report warnings for all checks *except* for SA01
