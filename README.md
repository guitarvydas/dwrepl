# dwrepl
Test of a REPL for a simple DPL.

This experiment shows that a responsive REPL can be built for a DPL using a blunderbuss approach on modern hardware (3 processes using websockets).

This works using only a small amount of HTML and Python code. No further optimization is required.

# usage
- open a terminal window, run `make`
- open the file `ide.html` in a local browswer window
- open `test.drawio` in a local version of draw.io (https://app.diagrams.net/)
- type `test.drawio` in the browser's first input box
- type some text, say `asdf` into the browser's second input box, labelled `Input:`
- move the `?C` probe on the diagram
- select File>>Save or use the keyboard shortcut to save the drawing (Command-S on the Mac)
- observe the output and probe windows in the browser (the text should appear in 3 places: `Output:`, `Probe A` and `Probe C` 

# Code Repository

https://github.com/guitarvydas/dwrepl

## Overview of the code
The browser based GUI is in `ide.html`.

The websocket server and plumbing is in `main.py`. The code probably needs an overhaul (volunteers welcome :-), but, it works as it stands.

The test program source (diagram) is in `test.drawio`.

The diagram is saved in `.graphml` format by draw.io. The `test.drawio` graphml file is culled and spit out as `test.drawio.json` using `das2json/mac/das2json` which is a straight-forward use of an XML parser. The `test.drawio.json` file is inhaled by the Python script `main.py` and instantiated and run using `py0dws.py` and `ouptut.py`. `Py0dws.py` is essentially a mutual multi-tasking kernel written Python that treats each rectangle on the diagram as a software component with input and output ports. The kernel routes messages between the components in a straight-forward manner. The kernel is reminiscent of Python `async` and `await` style mutual multitasking, with the addition of queues for components that allow for multiple ports on each component. Little networks are composed by recursive instantiation of `Container` components, while actual code is stored, as Python, in `Leaf` components.

The result messages are queued up on the output ports of the top-level Container. These results are sent as text strings to the web browser IDE using websockets.

The source for `das2json` can be found in `https://github.com/guitarvydas/0D/tree/main/das2json` - the `0D` repository. `Das2json` is currently written in the Odin language, but should be straight-forward to port to most other languages. It is basically a straight-forward XML parser that discards all visual/graphical details (x, y, color, etc.) from the diagram, figures out containment (using x,y information), and leaves only the semantically interesting connection information.

## Tested on MacOS
Mac mini M3 running Sonoma 14.6.1.

To recompile the current version of `das2json`, an Odin compiler is required.

A version of `das2json` for Intel Apple exists. Versions have not been cross-compiled to other platforms, yet. It is hoped to rewrite `das2json` in the future using `t2t` (a parser and rewriter tool) or other XML parser libraries, obviating the need for an Odin compiler.

