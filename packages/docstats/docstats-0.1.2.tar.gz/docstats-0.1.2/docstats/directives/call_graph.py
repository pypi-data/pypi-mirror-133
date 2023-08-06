"""Generate Callgraphs for documentation."""

import os
import subprocess
from typing import List

from docutils.nodes import Node
from docutils.parsers.rst import Directive
from sphinx.ext.graphviz import graphviz
from sphinx.util.typing import OptionSpec

callgraph_count = 0


class CallGraphException(Exception):
    """Exception for callgraph class."""


class call_graph(graphviz):
    """A docutils node to use as a placeholder for the call graph."""


class CallGraph(Directive):
    """Generate a callgraph."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec: OptionSpec = {}

    def run(self) -> List[Node]:
        """Run the directive."""
        global callgraph_count

        if not os.path.exists("source/graphs"):
            os.makedirs("source/graphs")

        subprocess.run(
            [
                "code2flow",
                "../",
                "-o",
                f"source/graphs/callgraph_{callgraph_count}.dot",
                "--language",
                "py",
                "--quiet",
            ]
        )

        with open(
            f"source/graphs/callgraph_{callgraph_count}.dot", encoding="utf-8"
        ) as fp:
            dotcode = fp.read()

        callgraph_count += 1

        node = graphviz()

        node["code"] = dotcode
        node["options"] = {}

        return [node]
