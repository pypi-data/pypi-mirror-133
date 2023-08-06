from setuptools import setup

name = "types-Markdown"
description = "Typing stubs for Markdown"
long_description = '''
## Typing stubs for Markdown

This is a PEP 561 type stub package for the `Markdown` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `Markdown`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/Markdown. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `032e6ee90cbb938259a2aa2183966502de19108e`.
'''.lstrip()

setup(name=name,
      version="3.3.11",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      install_requires=[],
      packages=['markdown-stubs'],
      package_data={'markdown-stubs': ['__init__.pyi', '__meta__.pyi', 'blockparser.pyi', 'blockprocessors.pyi', 'core.pyi', 'extensions/__init__.pyi', 'extensions/abbr.pyi', 'extensions/admonition.pyi', 'extensions/attr_list.pyi', 'extensions/codehilite.pyi', 'extensions/def_list.pyi', 'extensions/extra.pyi', 'extensions/fenced_code.pyi', 'extensions/footnotes.pyi', 'extensions/legacy_attrs.pyi', 'extensions/legacy_em.pyi', 'extensions/md_in_html.pyi', 'extensions/meta.pyi', 'extensions/nl2br.pyi', 'extensions/sane_lists.pyi', 'extensions/smarty.pyi', 'extensions/tables.pyi', 'extensions/toc.pyi', 'extensions/wikilinks.pyi', 'inlinepatterns.pyi', 'pep562.pyi', 'postprocessors.pyi', 'preprocessors.pyi', 'serializers.pyi', 'treeprocessors.pyi', 'util.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Typing :: Stubs Only",
      ]
)
