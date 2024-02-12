# Configuration file for the Sphinx documentation builder.
import tomli


# -- Project information
def _get_project_meta() -> dict[str, str]:  # lying abour return type
    with open('../../pyproject.toml', mode='rb') as pyproject:
        return tomli.load(pyproject)['tool']['poetry']


pkg_meta = _get_project_meta()
project = pkg_meta['name']
author = pkg_meta['authors'][0]
copyright = author

# The short X.Y version
version = pkg_meta['version']
# The full version, including alpha/beta/rc tags
release = version

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'myst_parser',
    'autoapi.extension',
]

todo_include_todos = True

autodoc_typehints = 'description'
autoapi_dirs = ['../../horiba_sdk']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_book_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
