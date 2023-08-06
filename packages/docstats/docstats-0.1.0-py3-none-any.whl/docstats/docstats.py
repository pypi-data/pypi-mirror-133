from __future__ import annotations
from typing import Any

from docutils import nodes

from sphinx.ext.graphviz import render_dot_html, render_dot_latex, render_dot_texinfo

from .directives.call_graph import CallGraph, call_graph

def skip(self: Any, node: Any) -> None:
    raise nodes.SkipNode

def setup(app):
    app.setup_extension('sphinx.ext.graphviz')

    app.add_node(
        call_graph,
        latex=(render_dot_latex, None),
        html=(render_dot_html, None),
        text=(skip, None),
        man=(skip, None),
        texinfo=(render_dot_texinfo, None))
    app.add_directive('callgraph', CallGraph)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
    }
