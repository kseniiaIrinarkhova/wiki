#Markdown
Markdown is a light text markup format and a processor to convert that to HTML. The originator describes it as follows:

Markdown is a text-to-HTML conversion tool for web writers. Markdown allows you to write using an easy-to-read, easy-to-write plain text format, then convert it to structurally valid XHTML (or HTML).

-- [http://daringfireball.net/projects/markdown/](http://daringfireball.net/projects/markdown/)

This (**markdown2**) is a fast and complete Python implementation of *Markdown*. It was written to closely match the behaviour of the original Perl-implemented Markdown.pl. Markdown2 also comes with a number of extensions (called "extras") for things like syntax coloring, tables, header-ids. See the "Extra Syntax" section below. "markdown2" supports all Python versions 3.5+ (and pypy and jython, though I don't frequently test those).

There is another Python markdown.py. However, at least at the time this project was started, markdown2.py was faster (see the Performance Notes) and, to my knowledge, more correct (see Testing Notes). That was a while ago though, so you shouldn't discount Python-markdown from your consideration.

Follow @trentmick for updates to python-markdown2.