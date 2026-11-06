<h1 align="center">SynapseWrite</h1>
<p align="center"><b>A word processor that is one neural network.</b><br>Nobody trained it. Every weight was written on purpose.</p>

<p align="center"><img src="docs/figures/hero.gif" width="860" alt="SynapseWrite running in a browser: typing, styles, fonts, bold, italic and ribbon tabs"></p>

<p align="center"><i>Recorded from the real app through real browser events. The page is only a canvas and a hidden text field for phone keyboards. No HTML layout, CSS styling, canvas drawing or font API makes this image: the network outputs an RGBA tensor, and the glue displays it.</i></p>

| | |
|---|---|
| **Neurons** | 450,104, in 73 named sub-networks (one is currently empty) |
| **Connections** | 1,702,201: 946,543 that push values and 755,658 that are read lazily |
| **Depth** | 175 layers within one tick |
| **Control states** | 3,690 one-hot state neurons |
| **Non-network code at run time** | 81 lines of glue, 140 lines of inference engine |
| **Deployment** | one static HTML file, about 3.2 MB |
| **Training code** | none: no data, loss, gradient, search or fitting |

SynapseWrite follows the [Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/) approach: reason about what each layer must compute, then write the weights that compute it. A deterministic Python generator writes those weights. After that, Python is gone. The browser runs inference, plus the small glue described below.

It is an independent project with its own name and icons, modeled on the features and look of Microsoft Word. It is not affiliated with or endorsed by Microsoft and contains no Microsoft assets.

## Contents

[One tick](#the-whole-program-is-one-function) · [The equation](#the-equation-explained) · [Neurons](#from-neurons-to-logic) · [Control flow](#control-flow-a-token-in-the-weights) · [Sparsity](#why-half-a-million-neurons-can-feel-instant) · [Memory](#memory-the-network-holds-the-pointers) · [The screen](#the-screen-is-also-an-input) · [Text](#how-a-letter-gets-drawn) · [File formats](#file-formats-are-networks-too) · [Connections](#how-everything-is-connected) · [Every sub-network](#every-sub-network-and-why-it-exists) · [Boundaries](#what-is-not-the-network) · [Building](#build-it) · [Verification](#how-it-is-checked) · [Status](#status)

## The whole program is one function

Each key press, click, mouse move or timer signal starts ticks. A tick is one pass through the same network:

```
(last screenshot, event vector, memory reads, recurrent state)
        -> (next screenshot, memory operations, recurrent state, timer request, halt)
```

<p align="center"><img src="docs/figures/tick_loop.svg" alt="Animated diagram of one tick"></p>

The glue repeats ticks until the network's halt neuron fires, then waits for the next event. The screenshot is not a wide input layer: the network asks for one pixel at a time through a read port, plus block copies for the pointer and glyph work. Typing a letter takes about 65 ticks. Nothing about what a key means is known outside the network: the glue passes along the code units of the browser's key name, and neurons decide the rest.

The engine evaluates this rule, and nothing more:

```
v_i(t) = act_i( bias_i + sum over earlier layers  w_ji * v_j(t)
                       + sum over recurrent edges w_ji * v_j(t-1) )
```

## The equation, explained

Everything the app does comes from repeating one equation. You do not need a machine learning background to follow it, only the idea of a list of numbers and a table of numbers.

```
v(t) = σ( b + F·v(t) + R·v(t-1) + u(t) )
```

<p align="center"><img src="docs/figures/ann_structure.png" width="900" alt="The equation drawn with the real vector, matrices and activations from the weight file"></p>

*This figure is drawn from the shipped weight file. Each dot in a square is a group of real connections.*

### The pieces

**A neuron is one number, plus a simple rule for updating it.** The app has 450,104 of them. One holds the caret's position, for example, and another is 1 only while a particular step of the program is running.

| Symbol | In plain words | Size |
|---|---|---|
| `v(t)` | The state vector: a list of every neuron's value at tick `t`. Almost all of them are 0 at any moment. | 450,104 numbers |
| `t` | The tick count. One tick is one update of the whole list. A key press takes roughly 65 to 150 ticks. | |
| `F` | The same-tick table. The entry at row `i`, column `j` says how strongly neuron `j` feeds neuron `i` within this tick. | 450,104 by 450,104, with 1,656,356 entries that are not 0 |
| `R` | The last-tick table. It works the same way, but reads neuron values from the previous tick. | The same size, with 45,845 entries that are not 0 |
| `b` | A fixed offset for each neuron, called its bias. | 450,104 numbers |
| `u(t)` | What arrives from outside this tick: an event from the glue, or data read from memory. | Mostly 0 |
| `σ` | Each neuron's activation: a simple rule applied to its total. | One rule per neuron |

The two tables are programmed, not learned. Each of their entries was written by the generator for a reason. Their entries that are not 0 fill less than 0.001 percent of each table, and they only ever use about 10,000 different values.

### Reading it from the inside out

To update one neuron, do three things:

1. **Add up what it receives.** That is its bias, plus each input neuron's value times its weight, plus anything arriving from outside.
2. **Apply its rule.** Most neurons use one of the first two below.
3. **Store the result** as that neuron's new value.

| Rule | Output | Neurons | Used for |
|---|---|---:|---|
| Step | 1 if the total is above 0, otherwise 0 | 218,815 | Yes or no decisions |
| ReLU | The total if it is above 0, otherwise 0 | 205,715 | Passing a number through a gate |
| Identity | The total, unchanged | 23,904 | Adding numbers |
| Hold | Keeps its value, and adds any total to it | 1,670 | Registers that only remember |

The fourth rule is an engine detail. The generator writes three kinds of neuron, and the optimizer converts registers that do nothing but hold their value into this cheaper form.

### Why `v(t)` is on both sides

This looks circular, but it is not. The neurons are numbered so that each one reads only from neurons before it, which puts every entry of `F` below the diagonal of the table. So the first neuron can be calculated from outside inputs alone. The second can then use the first, and so on to the end.

<p align="center"><img src="docs/figures/equation_sweep.svg" alt="Animated three neuron example of filling in the vector from the top down"></p>

Here is that example written out, with an input of 5:

```
a = 5             a is 5
b = 10 × a        b is 50
c = a + b         c is 55
```

After the sweep, multiplying the table by the finished vector gives that same vector back. That is all the equation claims. It is like a spreadsheet, where a cell can use cells calculated before it, as long as no formula refers back to itself.

If you have seen numerical methods, this is forward substitution on a lower triangular system. Nothing is iterated, and there is no matrix to invert. Although the equation looks implicit, it is an explicit calculation.

### How the two tables differ

- **`F` is for computing.** It carries signals within a tick, through as many as 175 layers. Most of a neuron's work happens here. A layer is just a group of neurons at the same depth, so layer sizes vary widely.
- **`R` is for remembering.** It carries values from one tick to the next. A register is a neuron that feeds itself through `R`, which is how the network holds a number over time. It is also how control moves from one program step to the next.

Together, they make a recurrent network. Each tick takes the last state and the new input, then produces the next state:

```
v(t) = G( v(t-1), u(t) )
```

Here `G` is the feed-forward network formed by `b`, `F` and `σ`. Each tick is one direct step forward, and the ticks do not converge toward an answer. They are the steps of a program, and they end when one particular neuron, the halt neuron, becomes nonzero.

### A logic gate from one row

This shows how arithmetic becomes decisions. Say neuron `y` should pass a value `v` only when a control neuron `en` is 1. Give it these entries:

```
y = relu( v + en × 2^40 − 2^40 )
```

| `en` | Total | Output `y` |
|---:|---|---|
| 1 | `v + 2^40 − 2^40`, which is `v` | `v` |
| 0 | `v − 2^40`, which is far below 0 | 0 |

That is one row of `F`: a weight of 1 from `v`, a weight of 2^40 from `en`, a bias of −2^40, and a ReLU rule. With gates like this, the generator builds registers, comparisons, memory addressing and program flow.

### What is not in the equation

The equation updates neurons and nothing else. Three things sit around it:

- **Memory and the screen.** The document is stored in a separate memory bank. There are ports that treat particular neurons as an enable, an address and data. When an enable is nonzero, the engine carries out that read or write. Data that is read comes back through `u` on the next tick.
- **The glue.** It writes events into `u`, runs ticks until the halt neuron fires, and shows the screen.
- **A second clock.** Neurons for drawing text and for managing styles run as a separate block with no connections to the main block, shown by the amber lines in the figure. A call port pauses the main block, passes values over, runs the second block to completion and passes the results back.

## From neurons to logic

The generator writes three activation functions. (The engine has a fourth kind internally, an optimization for registers whose only job is holding their value.) The important building block is the gate, which lets a one-bit signal decide whether a value passes.

<p align="center"><img src="docs/figures/neuron_gate.svg" alt="Identity, step and ReLU neurons with an animated big-M gate"></p>

This is the actual generator code from [`gen/nn.py`](gen/nn.py), with spacing and a comment added. It is ordinary weight arithmetic:

```python
def gate(s, val, en):
    val = as_x(val); en = as_x(en)
    if val.is_const(): return en * val.c
    return s.relu(val + en*M - M)      # M = 2**40
```

With gates you can build multiplexers, registers (a neuron feeding itself through a recurrent edge), comparators, decision trees and memory addressing. Linear expressions fold into the next real neuron at build time, so `a + 2*b` costs no neuron of its own.

## Control flow: a token in the weights

The program counter is a one-hot vector. In each clock domain, exactly one state neuron holds 1, and its weights open the gates for that step. Many neurons can compute in the same tick, but control moves one step at a time, much like a processor.

<p align="center"><img src="docs/figures/fsm.svg" alt="Animated token moving through state neurons"></p>

Subroutines work too: a return register holds the id of the state to go back to, and a small dispatch layer decodes it. The build fails if two states share a name.

## Why half a million neurons can feel instant

Neurons rest at zero, and the engine only visits a neuron when something nonzero reaches it. Gated neurons are lazy: their value inputs are read only if the gate opens. This is real data from the shipped weights, one frame per group of ticks. Watch the font outlines tile in the top left: it lights up only for a letter that has not been drawn before.

<p align="center"><img src="docs/figures/neural_activity.gif" width="860" alt="Neuron activity map for four events beside the screen output"></p>

<p align="center"><img src="docs/figures/event_cost.svg" alt="Bar chart: fired neurons per event, all under one percent"></p>

| Event | Ticks | Edges pushed | Neurons fired |
|---|---:|---:|---:|
| Type a letter | 65 | 2,435 | 1,371 |
| Type a new letter | 148 | 127,069 | 2,138 |
| Move the mouse | 10 | 51,232 | 1,598 |
| Click in text | 325 | 154,674 | 3,310 |
| Scroll one notch | 307 | 151,688 | 3,057 |
| Press Ctrl+B | 312 | 149,855 | 3,166 |
| Paste two lines | 436 | 387,104 | 4,308 |

Figures are from a short document at commit `9387767`. A long document costs more on events that repaint the whole view.

## Memory: the network holds the pointers

External memory is a passive tensor. The network produces every address, read, write, length and mask. The engine executes those signals and decides nothing.

<p align="center"><img src="docs/figures/memory_map.svg" width="760" alt="Memory bank map"></p>

Two timing rules shape the design: a read's data arrives on the tick after its address, and it lasts one tick. Much of the generator is careful scheduling around those two facts, much like programming a pipelined processor by hand.

## The screen is also an input

The output is RGBA, and the alpha channel is not transparency. It holds an object id. To answer "what did the user click?", the network reads the pixel under the pointer from its own last screenshot.

<p align="center"><img src="docs/figures/id_plane.png" width="900" alt="The screen tensor split into color channels and id channel"></p>

So buttons, tabs and menu rows need no table of rectangles: they paint their ids as they draw. For a click in text, the id finds the line, and a line table in memory gives the exact document position. The pointer shape comes from the same plane. On caret blink ticks, a small checker also reads the screen back and compares it to the line table, then repairs any damage it finds.

## How a letter gets drawn

There is no stored bitmap font, and no transform basis. Open font outlines are compiled straight into weights. Each outline edge is a neuron whose weights are that edge's line coefficients. A glyph is literally a small program made of neurons.

<p align="center"><img src="docs/figures/glyph_raster.gif" width="860" alt="Animation of an outline being converted to pixel coverage by edge neurons, ramps and winding"></p>

1. A binary tree over the glyph's outline heights selects the edges that cross the current sample line.
2. Each edge neuron computes `x = X0*s + m*(y - Y0)`, where `s` scales for the font size.
3. A shared bank of ramps, `R_q = relu(q - x)`, turns a crossing into pixel shares: `R_(q+1) - R_q`.
4. The signed sum is the winding number. A clamp makes it coverage.
5. Four sample lines accumulate into one pixel row.

The glyph unit runs in its own clock domain, entered through a call port while painting stalls. The style interner is the only other sub-network that works this way. Finished glyphs go to a cache in memory, tagged by face, size and character, so repeated letters skip the generator. That is why the font outlines tile stays dark for the second Q in the animation above.

Vertical snapping is a piecewise linear layer written from font metrics. Horizontal snapping is also written, but no font turns it on, because it looked worse when compared side by side. Eight open families ship: Carlito, Caladea, Arimo, Tinos, Cousine, Open Sans, Oswald and Caveat.

<p align="center"><img src="docs/figures/subnetwork_sizes.svg" alt="Bar chart of neurons by family of sub-networks; font outlines are 81 percent"></p>

The other 90,000 or so neurons hold the rest of text drawing and the entire word processor. The provenance record, [`PROVENANCE.md`](PROVENANCE.md), lists all 73 sub-networks with their purposes and generator files, and is regenerated by every build.

## File formats are networks too

Opening a `.docx` means inflating a zip file and parsing XML. Saving means writing XML, compressing it with deflate, computing CRC32 and assembling a zip. All of that is neurons.

<p align="center"><img src="docs/figures/docx_pipeline.svg" alt="Animated open and save pipelines"></p>

The same is true of PNG pictures and PDF export. The network also chooses the file name and tells the glue when to offer the download.

## How everything is connected

The whole app is one neural network: one graph of neurons, evaluated by one engine. A "sub-network" is a label on a set of those neurons, recorded by the generator so each neuron can be traced to its purpose. There is no boundary in the weights between them. The colored families in this figure are just categories for this README. The sub-networks are also not wired in a chain: they are built around a hub. This figure and the numbers below are decoded from the shipped weight file, and the engine ports are read from the same file.

<p align="center"><img src="docs/figures/network_wiring.svg" alt="Connection diagram from browser through glue, network families and hub, engine ports, memory and screen, back through glue"></p>

**The hub is where features meet.** The largest piece, `compiled control`, is where the generator compiles every state rule. If twenty features can write the caret, then the caret register has one sum here, with a gated term from each. So features rarely call each other. They set shared registers and drive shared ports, and a closed gate contributes exactly zero.

| Between | Connections |
|---|---:|
| Hub (control and wiring) and Reading files | 15,497 |
| Hub (control and wiring) and Laying out and painting the page | 14,274 |
| Hub (control and wiring) and Writing files | 8,250 |
| Changing the document and Hub (control and wiring) | 7,343 |
| Getting events in and Hub (control and wiring) | 6,068 |
| Drawing text and Laying out and painting the page | 3,860 |
| Laying out and painting the page and Writing files | 1,648 |
| Changing the document and Getting events in | 1,082 |
| Drawing text and Getting events in | 918 |
| Drawing text and Hub (control and wiring) | 912 |

Each row is the connection count between two families. These are the ten largest of 21 pairs.

**The glue sits only at the edges.** It connects to the network through the pieces below, and nowhere else.

| Glue piece | What crosses it | Network side, as measured |
|---|---|---|
| Event encoder | Event kind, 3 arguments, modifiers, day number | Input neurons in `bank and port wiring` |
| Key encoder | Code units of the key name, and its length | Input neurons in `bank and port wiring`, read by `raw event interpretation` |
| Byte encoders | File bytes, paste text and phone field text, written straight into the bank | `docx reader`, `png reader`, `paste` and `raw event interpretation` then read them |
| Tick loop | Calls the engine until the halt neuron fires | Halt neuron in `bank and port wiring` |
| Display | Copies changed rows of the screen tensor to the canvas | Screen ports driven by `bank and port wiring`, `glyph unit` and `pointer` |
| Timer | Sets a browser timer for the requested time | Timer neuron in `bank and port wiring` |
| Clipboard out | Sends a text the network placed in the bank | Length neuron in `bank and port wiring`, hold in `raw event interpretation` |
| Clipboard in | Asks the browser for text | Request neuron in `range walker` |
| Save file | Reads bytes and a name from the bank, and offers a download | `file output command` |
| File pickers | Opens a picker for a document or a picture | Request neurons in `docx reader` and `png reader` |
| Browser defaults | Lets a key do its normal action, or holds mouse moves for a frame | `raw event interpretation` |
| Keyboard field | Sets field text and focus, for phones | `raw event interpretation` |
| Added words | Copies the added word list to browser storage | Length neuron in `docx reader rv_a5` |

**The engine ports are the network's only way to act.** There are 24 memory read ports, 26 memory write ports, 5 rectangle ports, 4 patch ports, 3 copy ports, 1 screen pixel read port, 2 style read ports and 2 call ports. The two call ports enter the glyph unit and the style interner, which each run in a second clock domain while the main one stops.

Here is every connection, at the level of single sub-networks. Each row sends to each column.

<p align="center"><img src="docs/figures/network_matrix.svg" alt="Matrix of connections between all sub-networks"></p>

Two things to keep in mind when reading it. The build merges duplicate neurons, and a merged neuron is credited to just one sub-network. So a line between two unrelated names, such as `png reader` and `compiled control`, can be logic they share. That is also why a few reader and writer names light up slightly on a key press. The raw data is in [`docs/figures/src/connections.json`](docs/figures/src/connections.json).

<!-- networks:start -->
## Every sub-network, and why it exists

The build traces each neuron to one of 73 named sub-networks. This is the whole list, with neuron counts from the current build. Names are the exact labels in [`PROVENANCE.md`](PROVENANCE.md), and some keep working labels from when they were written (`a4`, `rv a3`, `tier 2`).

<p align="center"><img src="docs/figures/network_path.svg" alt="Animated path of a key press through the sub-networks"></p>

### Getting events in (15,334 neurons)

The browser reports raw facts, such as a key name or a button mask. Deciding what those facts mean is application logic, so it has to happen in neurons.

| Sub-network | Neurons | What it does | Why it exists |
|---|---:|---|---|
| `compiled control` | 9,427 | Holds every state rule, compiled together: the gated sums that give each register its next value, plus the return dispatchers. | This is where features actually meet. A register written by many features has one sum here, with one gated term per rule that writes it. |
| `rv a3 interaction` | 2,704 | Handles word and page motion, right click, autoscroll while dragging and the context menu. It also holds the later tier 1 features from `gen/t1_features.py`. | These editing motions need more than a single key rule, because they scan text and follow the pointer over many ticks. |
| `bank and port wiring` | 1,296 | Holds the shared wires that drive the memory, image and event ports, including the input neurons the glue writes into. | Ports are the only way out of the network. Several sub-networks use each port, so one place sums their addresses and enables. That avoids a duplicate port per feature. |
| `key handling` | 520 | Maps each key and modifier combination to an editing command. | Shortcuts are behavior, so they live in weights instead of a key table in the glue. |
| `shared control registers` | 451 | Holds editor state such as caret, selection and typing format, plus the comparators that order a selection. | Many features read the same state. Shared registers mean each feature does not keep its own copy that could fall out of step. |
| `screenshot hit test` | 378 | Reads the object id under the pointer from the last screen. For text, it then uses the line table in memory to find the document position. | The screen already knows which object was drawn where, so buttons and menus need no separate table of rectangles. |
| `raw event interpretation` | 313 | Turns key name code units, button masks, pointer types, field text and touch positions into cooked events. It also tells the browser whether its default action stands. | The glue is forbidden from knowing what Enter or a right click is. This network is what makes that rule possible. |
| `ribbon actions` | 155 | Maps a clicked button id to its command. | The ribbon has many targets. One map lets the pointer path stay the same for all of them. |
| `character maps` | 89 | Converts between Unicode and the internal character codes, using the Windows-1252 block. | Keeping internal codes small keeps glyph, metric and spelling tables small. Files and the clipboard still need Unicode. |
| `event dispatch` | 1 | One neuron left from the first dispatcher. It did not fire on the key presses we traced. | Routing now lives in `raw event interpretation` and the state rules. It is listed so that the record stays complete. |

### Changing the document (3,839 neurons)

These networks are the only ones that write document text. They all go through the same edit and undo paths, so everything stays undoable.

| Sub-network | Neurons | What it does | Why it exists |
|---|---:|---|---|
| `tier 4 features` | 699 | Implements tracked changes, fields, equations and mail merge. | These change what a run of text means, rather than how it looks. |
| `bulk edits` | 656 | Processes windows of many cells per tick for large formatting, copy, save, paste and find operations. | Going one cell per tick is too slow on a 100 page document. These walkers keep large operations usable. |
| `range walker` | 385 | Walks a selection for copy, cut, delete and formatting. | Selections cross paragraphs and slots. One walker holds that hard logic, and each command just supplies the action. |
| `tier 2` | 357 | Implements style commands, paragraph commands, lists and typed font sizes. | These commands share paragraph records and a style table, so they are grouped around that data. |
| `a4 commands` | 320 | Implements repeat, format painter and keep rules, among others. | These are small commands that reuse existing registers, and each needs only a few rules. |
| `find and replace` | 279 | Runs a search automaton over the document, counts matches and replaces them. | Search needs its own scanning state, which is separate from the caret. |
| `find across paragraphs` | 231 | One matcher for queries that hold paragraph marks, shared by the replace walker, the match counter and the highlight. | A match that crosses a paragraph cannot be found inside one slot, so it needs state that follows the text across slots. |
| `paste` | 204 | Inserts clipboard text and splits it into paragraphs. | Pasted text arrives as a flat vector of code units, and the document stores paragraphs. |
| `edit primitives` | 196 | Inserts and deletes characters and paragraphs, and logs each change for undo. | It is the single choke point for edits, so undo cannot be bypassed by accident. |
| `a4 tabs` | 160 | Handles tab stops. | A tab has no fixed width. Its advance depends on the current position, so layout needs a dedicated rule. |
| `undo` | 107 | Walks the log backward and forward to undo and redo. | The log format is shared, so any feature that logs correctly gets undo with no extra network. |
| `clipboard formatting` | 103 | Keeps the style cells and paragraph records of the copy, and restores them when the pasted text equals that copy. | The system clipboard carries only text here. So the network keeps formatting in its own memory, and uses it when the pasted text matches. |
| `spell dictionary` | 67 | Walks a word automaton held as a read only table, with one read per painted letter, and marks misspelled words. | An automaton checks a word at one step per letter. The table is built from the word list by merging identical subtrees, with no fitting. |
| `style interner` | 53 | Finds or adds a style record in the interned table, in its own clock domain. | Each character stores a short index instead of a full record. That makes the text compact and makes comparing two styles a single check. |
| `tier3` | 22 | Holds the remaining tier 3 commands, plus undo for their operations. | It connects tier 3 features to the shared undo log. |

### Laying out and painting the page (7,874 neurons)

These networks decide where everything goes, then draw it.

| Sub-network | Neurons | What it does | Why it exists |
|---|---:|---|---|
| `chrome` | 1,893 | Draws the caret, scrollbar and status bar, and handles autoscroll. | These change on most events and must update without repainting the page. |
| `layout and paint` | 1,039 | Walks paragraphs and places lines and words. It draws text, selection and pictures. | It is the main drawing loop. Most features add to this one walk, so they do not repaint separately. |
| `pictures` | 926 | Draws picture handles, resizes pictures by resampling, writes PNG and reads pictures from a file. | A picture is the one document object that is not text, so it has its own storage and drawing path. |
| `a4 merge` | 639 | Handles merged table cells. | Merging breaks the simple grid that the table walker assumes, so it needs its own rules. |
| `tables` | 627 | Scans tables, inserts them, edits rows and columns, applies shading, and handles border hit zones and dragging. | A table has structure that must stay consistent as rows and columns change, and borders are also click targets. |
| `zoom` | 437 | Handles zoom levels from 50 to 150 percent and read mode, maps paint to the screen at the chosen scale, and runs the status bar controls. | Paint works in page coordinates. This keeps the many drawing paths unaware of the zoom level. |
| `a4 borders` | 387 | Draws paragraph borders and shading, on screen and in PDF. | Neighboring paragraphs can join borders, so this cannot be drawn one paragraph at a time. |
| `a4 ruler` | 307 | Draws the ruler and handles dragging its markers. | The ruler both displays and edits paragraph properties, so it needs its own drawing and pointer logic. |
| `line breaking` | 290 | Finds where lines break, and handles alignment. | Every paragraph needs it, and it runs on each edit, so it has to be small. |
| `a4 pagenum` | 254 | Handles page number formats and section start values. | Page numbers depend on sections, and they have to come out the same on screen and in a PDF. |
| `notes and balloons` | 253 | Draws wrapped text, comment balloons and footnotes. | These flow outside the normal text column, and they take space from the page or margin. |
| `table of contents` | 175 | Builds and updates the table of contents. | It has to scan headings and their final page numbers, which are known only after layout. |
| `ribbon display list` | 150 | One sequencer that plays draw records for the ribbon, menus and labels from read only memory, one item per tick. | Drawing a ribbon is data more than logic. Its neurons are shared by every list, and the lists themselves cost no neurons. |
| `pointer` | 118 | Draws the mouse pointer, saves and restores the colors under it, and chooses its shape from the screen. | The output is one image, with no system cursor over it. So the network has to draw the pointer and clean up after it. |
| `headers and footers` | 112 | Holds header and footer strings and their edit bar. | They repeat on each page, and they are edited separately from the main text. |
| `sections` | 106 | Holds section records, section breaks and page setup. | Page size, margins and columns can change partway through a document. |
| `canvas look` | 82 | Draws the page shadow and the canvas around the page. | This is the appearance around the page, kept separate because it does not depend on the document. |
| `a4 keep` | 56 | Applies keep with next and keep lines during pagination. | It has to add up the height a paragraph must share a page with before placing its first line. |
| `screen check` | 23 | Compares one line of the id plane with the line table on each blink tick, and repairs it by repainting. | The project requires checking the screen against document state. This catches drawing damage as the app runs. |

### Drawing text (410,392 neurons)

This is the largest family. It is what replaces a font engine. The method is described in [How a letter gets drawn](#how-a-letter-gets-drawn).

| Sub-network | Neurons | What it does | Why it exists |
|---|---:|---|---|
| `glyph weights (outline edges)` | 360,490 | Holds the font outlines as edge neurons, one small program per glyph. | This is the font itself, written as weights. It accounts for most of the neurons, since eight families with their faces hold many edges. |
| `glyph metrics` | 17,932 | Holds advance widths and kerning as decision trees. | Layout needs widths for each character, and it should not have to draw a glyph to learn one. |
| `glyph pixel records` | 16,534 | Records a small glyph drawn black on white, so that later draws take one read and one patch. | Most repaint cost was glyph rows. Replaying a record is much cheaper for the common case of plain text. |
| `glyph unit` | 7,116 | Runs the drawing of one glyph, in its own clock domain. | Paint can stall while a glyph is generated, and that keeps the paint loop simple. |
| `ramp bank` | 4,978 | Provides shared ramps, `R_q = relu(q - x)`, that turn a crossing into pixel shares. | Ramps are the same for all glyphs, so one bank serves every edge. Each glyph does not need its own. |
| `coverage` | 2,261 | Adds edge shares into pixel coverage. | It turns signed crossings into how much of a pixel is ink, which gives smooth edges. |
| `glyph network` | 634 | Selects and addresses a character cell for drawing. | It is the junction between layout and drawing, whichever way the glyph is produced. |
| `snapping layer` | 236 | Fits outline heights to the pixel grid for a given size. | Unsnapped text looks blurry at small sizes, so heights move to whole pixels using font metrics. Horizontal snapping is written, but no font uses it now, because it looked worse side by side. |
| `glyph geometry` | 159 | Scales outline coordinates by the drawn size. | A single set of weights can then serve any size, rather than storing outlines per size. |
| `row sequencer` | 29 | Steps the glyph unit through the rows of a character. | Coverage builds one sample line per tick, so something has to count them. |
| `glyph store` | 17 | Keeps drawn glyphs in memory and copies them to the screen. | Generating a glyph costs far more than copying one, and most letters repeat. |
| `glyph patch` | 6 | Assembles coverage and color into a patch for the patch port. | Text color is applied here, so a cached glyph works in any color. |
| `stem units` | 0 | Would hold stem positions for horizontal snapping. It has no neurons in the current build, because no font turns that on. | It is listed so that the provenance record stays complete. |

### Reading files (6,787 neurons)

Each of these exists because no parser library is allowed. XML, zip and PNG bytes are consumed one state at a time.

| Sub-network | Neurons | What it does | Why it exists |
|---|---:|---|---|
| `docx reader` | 1,847 | Unzips the file, inflates it and parses the document XML. | It is the core of opening a file. The goal requires that networks do parsing and decompression. |
| `docx reader rv_a5` | 1,463 | Improves fidelity on files from other programs: nested tables, row spans, spacing and truncated content. It also holds spell suggestions and the saved list of added words. | Real files use forms that a simple reader misses. The spelling parts sit here only because of where they were added in the generator. |
| `docx reader tier 4` | 1,368 | Reads tracked marks and fields. | These wrap ordinary runs in extra elements, so they add state to the parser. |
| `docx reader notes` | 819 | Reads footnote, comment and header parts. | Each of these has its own XML part that must be connected back to the main text. |
| `docx reader tier 2` | 543 | Reads styles, numbering, and run and paragraph properties. | Formatting in `.docx` is scattered across several parts and elements. |
| `png reader` | 373 | Decodes PNG files to pixel words, with limits on bad input. | Pictures in a `.docx` are usually PNG, and they have to become pixels the network can draw. |
| `a4 docx` | 268 | Reads and writes the paragraph properties added by the commands above. | Anything the app can do must survive a save and open, so features carry their own file code. |
| `docx reader tier 3` | 106 | Adds walking between the parts of a file. | Tier 3 content lives in separate parts of the zip file. |

### Writing files (5,878 neurons)

Saving runs the same idea in reverse. The network produces every byte, and the glue only offers the download.

| Sub-network | Neurons | What it does | Why it exists |
|---|---:|---|---|
| `docx crc` | 2,775 | Computes CRC32 of the bytes written to the zip file. | Zip readers reject a file with a wrong checksum. It holds four 256 entry tables as weights, so it can process four bytes at once. |
| `pdf writer` | 1,239 | Writes PDF objects, text and pictures. | Print to PDF is in the goal, and PDF has its own structure of objects and offsets. |
| `docx writer` | 1,046 | Writes the document XML parts. | A saved file needs XML text with the values of this document filled in. |
| `docx writer tier 3` | 306 | Writes section properties, tabs, markers, comments, notes, headers and footers. | These features add elements and whole parts to the saved file. |
| `docx deflate` | 242 | Compresses with LZ77 and fixed Huffman codes. | `.docx` files are compressed zip files, and compression has to happen in the network too. |
| `zip container` | 210 | Keeps the member table, and writes the central directory and table XML. | The directory at the end of a zip file has to list the size and offset of each part. |
| `pdf tables` | 55 | Writes PDF page size, table rules and shading. | Table lines are drawn as PDF commands, not as characters. |
| `file output command` | 5 | Selects the length, data start and file name that the glue saves. | The glue must not decide what to save, or under what name. It reads these neurons and acts. |

<!-- networks:end -->

## What is not the network

<p align="center"><img src="docs/figures/glue_boundary.svg" alt="Network logic compared with the glue and engine"></p>

The rule is that glue may not branch on, parse, format or interpret application data. It is enforced, not just promised. [`test/audit.py`](test/audit.py) holds an exact allow list of every `if` condition and string literal in the glue, and bans text parsing calls and drawing APIs. Anything new has to be argued for in that file.

Three things run outside the network, and they are all plumbing: the WASM inference engine, the event and byte encoding, and the commands the network raises by name (save this file, set this timer, focus this field). The glue also keeps the spell checker's added words in browser storage when the network says to.

## How it is built

<p align="center"><img src="docs/figures/build_pipeline.svg" alt="Animated build pipeline"></p>

Weights compress well because they recur. Neurons are stored in layer order as small integer deltas, weights index a table of distinct values, duplicate neurons are merged, and dead ones are removed. Display lists hold the ribbon, menus and labels in read only memory, played by one sequencer. The page also carries read only tables for strings, the spell automaton and PDF fonts.

## Build it

You need clang with the wasm32 target, Python 3 with `fonttools`, `numpy` and `pillow`.

```bash
git clone https://github.com/dirktheeng/SynapseWrite.git
cd SynapseWrite
./make.sh
# then open build/index.html in a browser
```

To run the tests, add Node with Playwright. Saved-file checks also use LibreOffice.

```bash
NODE_PATH=$(npm root -g) node test/e2e.js
python3 test/audit.py
```

## How it is checked

Tests drive the app only through events, and they judge only output images and saved files.

| Check | What it shows | Last run at `9387767` |
|---|---|---|
| `test/e2e.js` | Editing, formatting and interaction, by comparing screens | 210 of 210 |
| `test/audit.py` | Glue and engine hold no application logic, no training code, provenance complete | 67 of 67 |
| `test/a5_docx.js` | Foreign `.docx` features survive, and opening stays cheap | passing |
| `test/roundtrip.js` | Save then open is pixel identical, including after LibreOffice | passing |
| `test/touch.js` | Touch scrolling and on-screen keyboard behavior | passing |
| `test/imp3.js` | Zoom, find across paragraphs, formatted clipboard, exact line heights | 49 of 49 |

More suites cover tables, pictures, fonts, PDF, tracked changes, equations and bulk edits. Fuzz tests run the real weights on a checked engine build that traps out-of-bounds memory, two active state tokens and non-boolean logic.

### Latency

Measured in headless Chromium on a CPU through WASM, on a long test document at `9387767`:

| Action | Time |
|---|---:|
| Type at the end of a long document | under 1 ms |
| Select all | 54 ms |
| Jump to top | 36 ms |
| Press Enter at the top of a long document | 35 ms |
| Undo | 38 ms |
| First paint of a page in a new font, 11 pt | 62 to 85 ms |

The project's target is under 100 ms from event to frame, at 1280 by 800. It has not been measured on a mid-range GPU.

## Status

Every feature is tracked in [`PARITY.md`](PARITY.md). "Passed" means an automated test passed, not that behavior was confirmed against Word.

| Tier | Scope | Passed | Partial |
|---|---|---:|---:|
| 1 | Ribbon, rulers, typing, selection, undo, clipboard, find | 8 | 7 |
| 2 | Formatting, styles, fonts, lists, line breaking, pagination | 8 | 4 |
| 3 | Tables, images, headers, sections, columns, footnotes, comments | 7 | 1 |
| 4 | Track changes, merge, equations, fields, spell check, PDF, `.docx` | 6 | 4 |

**Known gaps, stated plainly:**

- **Not verified in real Word.** No copy of Word has been used, so there are no pixel comparisons against Word, and saved `.docx` files have only been checked with LibreOffice and file-format checks.
- **Only tested in Chromium.** Current Firefox and Edge are targets, but they are untested.
- **Clipboard formatting works only inside the app.** Other programs receive plain text.
- **Zoom stops at 150 percent,** and there are no custom colors or user-created styles yet.
- **Greedy line breaking only,** with no hyphenation.

## Repository tour

| Path | What is there |
|---|---|
| `gen/nn.py` | Neuron, gate, register and state machine primitives |
| `gen/app.py` | The application network and its memory map |
| `gen/glyphnet.py`, `gen/rom.py` | The glyph unit, and font outline loading |
| `gen/docx_read.py`, `gen/t2_write.py`, `gen/pdf_write.py` | File format networks |
| `gen/ui.py`, `gen/rv_a9_dl.py` | Ribbon and menu contents, and the sequencer that plays them |
| `gen/t*_features.py`, `gen/rv_*.py` | Feature sub-networks |
| `host/engine.c`, `host/glue.js` | All the non-network run-time code |
| `test/` | Event-driven suites, fuzzing, audit and profilers |
| `docs/figures/src/` | Scripts that generate this README's figures |
| `PROGRESS_*.md` | Verbose build logs: what was tried, and each result |

## License

The code is under the [MIT License](LICENSE). The fonts in `fonts/` keep their own licenses, included with each family, and the word list keeps its notice in `gen/words_en.COPYRIGHT`.
