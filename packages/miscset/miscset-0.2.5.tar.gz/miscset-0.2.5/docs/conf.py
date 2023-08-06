# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import miscset
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'miscset'
copyright = '2021, Sven E. Templer'
author = 'Sven E. Templer'

# The full version, including alpha/beta/rc tags
release = miscset.version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'm2r2',
    'sphinx_exec_code',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bizstyle'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

source_suffix = ['.rst', '.md']

# enable autosummary to recurse modules and generate documentation
# documentation: https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html
# fixes in templates from: https://stackoverflow.com/questions/2701998/sphinx-autodoc-is-not-automatic-enough/62613202#62613202
autosummary_generate = True

# enable documentation for __init__ method in classes
#autoclass_content = 'both'

# link to python stdlib documentation via intersphinx
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
# https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cross-referencing-python-objects
intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}


autodoc_default_options = {
    'private-members': True,
    'undoc-members': True
}