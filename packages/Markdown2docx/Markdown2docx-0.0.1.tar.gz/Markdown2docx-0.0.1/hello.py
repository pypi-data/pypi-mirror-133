#!/usr/bin/env python3

from PreprocessMarkdown2docx import PreprocessMarkdown2docx
import Markdown2docx as m2

project = 'hello'
ppm2w = PreprocessMarkdown2docx(project)
macros = ppm2w.macros
markdown = ppm2w.get_all_but_macros()
markdown = ppm2w.do_substitute_tokens(markdown)
markdown = ppm2w.do_execute_commands(markdown)
project = m2.Markdown2docx(project, markdown)
project.eat_soup()
project.write_html()  # optional
project.save()
