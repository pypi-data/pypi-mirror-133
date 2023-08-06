"""Generate Callgraphs for documentation."""

import subprocess
from typing import List

from docutils.nodes import Node
from docutils.parsers.rst import Directive

from sphinx.ext.graphviz import graphviz
from sphinx.util.typing import OptionSpec

callgraph_count = 0

class CallGraphException(Exception):
    pass

class call_graph(graphviz):
    """A docutils node to use as a placeholder for the call graph."""
    pass

class CallGraph(Directive):
    """Run when the inheritance_diagram directive is first encountered."""
    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: OptionSpec = {
    }

    def run(self) -> List[Node]:
        global callgraph_count

        subprocess.run(
            ["code2flow", ".", 
             "-o", f"source/_static/callgraph_{callgraph_count}.dot", 
             "--language", "py"])

        with open(f"source/_static/callgraph_{callgraph_count}.dot", encoding='utf-8') as fp:
            dotcode = fp.read()

        callgraph_count += 1

        node = graphviz()

        node['code'] = dotcode
        node['options'] = {}

        return [node]
