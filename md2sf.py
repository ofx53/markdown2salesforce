#!/usr/bin/env python3


import os

import click
import mistune
from mistune.scanner import escape
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


class sf_html_render(mistune.HTMLRenderer):
    # This is a custom mistune extension that will override the default
    # behavior of several inline block element handlers to allow them to emit
    # the HTML needed by Saleforce's Knowledge system
    def codespan(self, text):
        """override the default `code` block handler"""
        return '<code style="font-size:1em;color:#00f;">' + escape(text) + "</code>"

    def paragraph(self, text):
        """override the default paragraph handler"""
        return "<p>" + text + "</p>\n"

    def block_code(self, code, lang=None):
        """inject the correct `code` block handlers for styling"""
        html_start = '<pre class="ckeditor_codeblock">'
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return html_start + highlight(code, lexer, formatter)+ "</pre>\n"
        else:
            return html_start + escape(code) + "</pre>\n"

        
        #return '<pre><code>' + mistune.escape(code) + '</code></pre>'


@click.command(help="Plese supply the path to a KB article in Markdown format to parse")
@click.argument("filename", type=click.Path(exists=True, readable=True), nargs=1)
def main(filename):

    with open(filename) as sf_kb:
        sf_kb_file = sf_kb.read()

    sf_html = open(os.path.splitext(filename)[0] + ".html", "w")

    with open('/home/xouimet/Documents/Dev/Random_scripts/markdown2salesforce/cssdata.txt') as sf_kb:
        css_start = sf_kb.read()
    sf_html.write(css_start)

    markdown = mistune.create_markdown(renderer=sf_html_render())
 
    
    sf_html.write(markdown(sf_kb_file))
    sf_html.write('\n</body>\n</html>')

if __name__ == "__main__":
    main()
