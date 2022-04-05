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
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

import datetime
import os
import sys
import urllib



# -- Project information -----------------------------------------------------

project = 'Open edX'
copyright = '2022, TCRIL'
#author = 'Mark Hoeber'

# The full version, including alpha/beta/rc tags
#release = '1.0'
import edx_theme


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinxcontrib.yt', 'sphinx.ext.autosectionlabel',  
  'sphinx_toolbox.collapse', 'sphinxcontrib.images', 'sphinx_panels']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'edx_theme'
#html_theme_path = [edx_theme.get_html_theme_path()]
#html_favicon = os.path.join(html_theme_path[0], 'edx_theme', 'static', 'css', 'favicon.ico')

html_theme = 'sphinx_book_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

images_config = {
   'default_image_width': '50%'
}

rst_epilog = """
.. include:: /substitutions.txt
"""
html_sidebars = {
    "reference/blog/*": [
        "sidebar-logo.html",
        "search-field.html",
        "postcard.html",
        "recentposts.html",
        "tagcloud.html",
        "categories.html",
        "archives.html",
        "sbt-sidebar-nav.html",
    ]
}

panels_add_bootstrap_css = False

# Fix build on RTD
# https://github.com/sphinx-contrib/images/issues/22

def monkeypatch_method(cls, fname=None):
    def decorator(func):
        local_fname = fname
        if local_fname is None:
            local_fname = func.__name__
        setattr(func, "orig", getattr(cls, local_fname, None))
        setattr(cls, local_fname, func)
        return func
    return decorator

import sphinx.application

@monkeypatch_method(sphinx.application.Sphinx)
def add_node(self, node, override=False, **kwds):
    if 'html' in kwds and 'epub' not in kwds:
        kwds['epub'] = kwds['html']
    return add_node.orig(self, node, override, **kwds)