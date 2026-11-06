<h1 align="center">SynapseWrite</h1>
<p align="center"><b>A word processor that is one neural network.</b><br>Nobody trained it. Every weight was written on purpose.</p>

<p align="center"><img src="docs/figures/hero.gif" width="860" alt="SynapseWrite running in a browser: typing, styles, fonts, bold, italic and ribbon tabs"></p>

<p align="center"><i>Recorded from the real app through real browser events. There is no HTML, CSS, DOM text, canvas drawing or font API behind this image: the network outputs an RGBA tensor and the page displays it.</i></p>

| | |
|---|---|
| **Neurons** | 443,759, in 68 named sub-networks |
| **Edges** | 941,650, in 166 layers |
| **Control states** | 3,499 one-hot state neurons |
| **Non-network code at run time** | 81 lines of glue, 140 lines of inference engine |
| **Deployment** | one static HTML file, about 3.2 MB |
| **Training code** | none: no data, loss, gradient, search or fitting |

SynapseWrite follows the [Weight-Space Programming](https://rikiyat.github.io/blog/weight-space-programming/) approach: reason about what each layer must compute, then write the weights that compute it. A deterministic Python generator writes those weights. After that, Python is gone, and the browser runs nothing but inference.

It is an independent project with its own name and icons, modeled on the features and look of Microsoft Word. It is not affiliated with or endorsed by Microsoft and contains no Microsoft assets.

## Contents

[One tick](#the-whole-program-is-one-function) · [Neurons](#from-neurons-to-logic) · [Control flow](#control-flow-a-token-in-the-weights) · [Sparsity](#why-half-a-million-neurons-can-feel-instant) · [Memory](#memory-the-network-holds-the-pointers) · [The screen](#the-screen-is-also-an-input) · [Text](#how-a-letter-gets-drawn) · [File formats](#file-formats-are-networks-too) · [Boundaries](#what-is-not-the-network) · [Building](#build-it) · [Verification](#how-it-is-checked) · [Status](#status)

## The whole program is one function

Each key press, click, mouse move or timer signal starts ticks. A tick is one pass through the same network:

```
(last screenshot, event vector, memory reads, recurrent state)
        -> (next screenshot, memory operations, recurrent state, timer request, halt)
```

<p align="center"><img src="docs/figures/tick_loop.svg" alt="Animated diagram of one tick"></p>

The glue repeats ticks until the network's halt neuron fires, then waits for the next event. Typing a letter takes about 150 ticks. Nothing about what a key means is known outside the network: the glue passes along the code units of the browser's key name, and neurons decide the rest.

The engine evaluates this rule, and nothing more:

```
v_i(t) = act_i( bias_i + sum over earlier layers  w_ji * v_j(t)
                       + sum over recurrent edges w_ji * v_j(t-1) )
```

## From neurons to logic

Three activation functions are enough. The important building block is the gate, which lets a one-bit signal decide whether a value passes.

<p align="center"><img src="docs/figures/neuron_gate.svg" alt="Identity, step and ReLU neurons with an animated big-M gate"></p>

This is the actual generator code, from [`gen/nn.py`](gen/nn.py). It is ordinary weight arithmetic:

```python
def gate(s, val, en):
    val = as_x(val); en = as_x(en)
    if val.is_const(): return en * val.c
    return s.relu(val + en*M - M)      # M = 2**40
```

With gates you can build multiplexers, registers (a neuron feeding itself through a recurrent edge), comparators, decision trees and memory addressing. Linear expressions fold into the next real neuron at build time, so `a + 2*b` costs no neuron of its own.

## Control flow: a token in the weights

The program counter is a one-hot vector. Exactly one state neuron holds 1, and its outgoing weights open the gates for that step.

<p align="center"><img src="docs/figures/fsm.svg" alt="Animated token moving through state neurons"></p>

Subroutines work too: a return register holds the id of the state to go back to, and a small dispatch layer decodes it. The build fails if two states share a name.

## Why half a million neurons can feel instant

Neurons rest at zero, and the engine only visits a neuron when something nonzero reaches it. Gated neurons are lazy: their value inputs are read only if the gate opens. This is real data from the shipped weights, one frame per group of ticks. Watch the font outlines tile in the top left: it lights up only for a letter that has not been drawn before.

<p align="center"><img src="docs/figures/neural_activity.gif" width="860" alt="Neuron activity map for four events beside the screen output"></p>

<p align="center"><img src="docs/figures/event_cost.svg" alt="Bar chart: fired neurons per event, all under one percent"></p>

| Event | Ticks | Edges pushed | Neurons fired |
|---|---:|---:|---:|
| Type a letter | 156 | 101,249 | 1,729 |
| Type a new letter | 154 | 127,065 | 2,118 |
| Move the mouse | 10 | 50,135 | 1,282 |
| Click in text | 313 | 197,526 | 2,620 |
| Scroll one notch | 295 | 194,538 | 2,364 |
| Press Ctrl+B | 300 | 192,710 | 2,477 |
| Paste two lines | 423 | 406,387 | 3,717 |

Figures are from a short document at commit `40524cd`. A long document costs more on events that repaint the whole view.

## Memory: the network holds the pointers

External memory is a passive tensor. The network produces every address, read, write, length and mask. The engine executes those signals and decides nothing.

<p align="center"><img src="docs/figures/memory_map.svg" width="760" alt="Memory bank map"></p>

Two timing rules shape the design: a read's data arrives on the tick after its address, and it lasts one tick. Much of the generator is careful scheduling around those two facts, much like programming a pipelined processor by hand.

## The screen is also an input

The output is RGBA, and the alpha channel is not transparency. It holds an object id. To answer "what did the user click?", the network reads the pixel under the pointer from its own last screenshot.

<p align="center"><img src="docs/figures/id_plane.png" width="900" alt="The screen tensor split into color channels and id channel"></p>

So hit testing needs no layout tree. Buttons, tabs, menu rows and text lines paint their ids as they draw. The pointer shape comes from the same plane. On caret blink ticks, a small checker also reads the screen back and compares it to the line table, then repairs any damage it finds.

## How a letter gets drawn

There is no stored bitmap font, and no transform basis. Open font outlines are compiled straight into weights. Each outline edge is a neuron whose weights are that edge's line coefficients. A glyph is literally a small program made of neurons.

<p align="center"><img src="docs/figures/glyph_raster.gif" width="860" alt="Animation of an outline being converted to pixel coverage by edge neurons, ramps and winding"></p>

1. A binary tree over the glyph's outline heights selects the edges that cross the current sample line.
2. Each edge neuron computes `x = X0*s + m*(y - Y0) + stem shift`, where `s` scales for the font size.
3. A shared bank of ramps, `R_q = relu(q - x)`, turns a crossing into pixel shares: `R_(q+1) - R_q`.
4. The signed sum is the winding number. A clamp makes it coverage.
5. Four sample lines accumulate into one pixel row.

The glyph unit runs in its own clock domain, entered through a call port while painting stalls. Finished glyphs go to a cache in memory, tagged by face, size and character, so repeated letters skip the generator. That is why the font outlines tile stays dark for the second Q in the animation above.

Vertical and horizontal snapping are piecewise linear layers written from font metrics. Eight open families ship: Carlito, Caladea, Arimo, Tinos, Cousine, Open Sans, Oswald and Caveat.

<p align="center"><img src="docs/figures/subnetwork_sizes.svg" alt="Bar chart of neurons by family of sub-networks; font outlines are 81 percent"></p>

The other 83,000 or so neurons are the entire word processor. The provenance record, [`PROVENANCE.md`](PROVENANCE.md), lists all 68 sub-networks with their purposes and generator files, and is regenerated by every build.

## File formats are networks too

Opening a `.docx` means inflating a zip file and parsing XML. Saving means writing XML, compressing it with deflate, computing CRC32 and assembling a zip. All of that is neurons.

<p align="center"><img src="docs/figures/docx_pipeline.svg" alt="Animated open and save pipelines"></p>

The same is true of PNG pictures and PDF export. The network also chooses the file name and tells the glue when to offer the download.

## What is not the network

<p align="center"><img src="docs/figures/glue_boundary.svg" alt="Network logic compared with the glue and engine"></p>

The rule is that glue may not branch on, parse, format or interpret application data. It is enforced, not just promised. [`test/audit.py`](test/audit.py) holds an exact allow list of every `if` condition and string literal in the glue, and bans text parsing calls and drawing APIs. Anything new has to be argued for in that file.

Three things run outside the network, and they are all plumbing: the WASM inference engine, the event and byte encoding, and the commands the network raises by name (save this file, set this timer, focus this field).

## How it is built

<p align="center"><img src="docs/figures/build_pipeline.svg" alt="Animated build pipeline"></p>

Weights compress well because they recur. Neurons are stored in layer order as small integer deltas, weights index a table of distinct values, duplicate neurons are merged, and dead ones are removed. Display lists hold the ribbon and menus in read-only memory, played by one sequencer.

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

| Check | What it shows | Last run at `40524cd` |
|---|---|---|
| `test/e2e.js` | Editing, formatting and interaction, by comparing screens | 210 of 210 |
| `test/audit.py` | Glue and engine hold no application logic, no training code, provenance complete | 67 of 67 |
| `test/a5_docx.js` | Foreign `.docx` features survive, and opening stays cheap | passing |
| `test/roundtrip.js` | Save then open is pixel identical, including after LibreOffice | passing |
| `test/touch.js` | Touch scrolling and on-screen keyboard behavior | passing |

More suites cover tables, pictures, fonts, PDF, tracked changes, equations and bulk edits. Fuzz tests run the real weights on a checked engine build that traps out-of-bounds memory, two active state tokens and non-boolean logic.

### Latency

Measured in headless Chromium on a CPU through WASM, on a long test document at `40524cd`:

| Action | Time |
|---|---:|
| Type at the end of a long document | about 2 ms |
| Jump to top | 44 ms |
| Press Enter at the top of a long document | 42 ms |
| Undo | 41 ms |
| First paint of a page in a new font, 11 pt | 41 to 79 ms |

The project's target is under 100 ms from event to frame, at 1280 by 800. It has not been measured on a mid-range GPU.

## Status

Every feature is tracked in [`PARITY.md`](PARITY.md). "Passed" means an automated test passed, not that behavior was confirmed against Word.

| Tier | Scope | Passed | Partial |
|---|---|---:|---:|
| 1 | Ribbon, rulers, typing, selection, undo, clipboard, find | 8 | 6 |
| 2 | Formatting, styles, fonts, lists, line breaking, pagination | 8 | 4 |
| 3 | Tables, images, headers, sections, columns, footnotes, comments | 7 | 1 |
| 4 | Track changes, merge, equations, fields, spell check, PDF, `.docx` | 6 | 4 |

**Known gaps, stated plainly:**

- **Not verified in real Word.** No copy of Word has been used, so there are no pixel comparisons against Word, and saved `.docx` files have only been checked with LibreOffice and file-format checks.
- **Only tested in Chromium.** Current Firefox and Edge are targets, but they are untested.
- **Clipboard is plain text.** Formatting is lost on copy and paste.
- **Greedy line breaking only,** with no hyphenation.

## Repository tour

| Path | What is there |
|---|---|
| `gen/nn.py` | Neuron, gate, register and state machine primitives |
| `gen/app.py` | The application network and its memory map |
| `gen/glyphnet.py`, `gen/rom.py` | The glyph unit, and font outline loading |
| `gen/docx_read.py`, `gen/t2_write.py`, `gen/pdf_write.py` | File format networks |
| `gen/ui.py` | Ribbon and menus |
| `gen/t*_features.py`, `gen/rv_*.py` | Feature sub-networks |
| `host/engine.c`, `host/glue.js` | All the non-network run-time code |
| `test/` | Event-driven suites, fuzzing, audit and profilers |
| `docs/figures/src/` | Scripts that generate this README's figures |
| `PROGRESS_*.md` | Verbose build logs: what was tried, and each result |

## License

The code is under the [MIT License](LICENSE). The fonts in `fonts/` keep their own licenses, included with each family, and the word list keeps its notice in `gen/words_en.COPYRIGHT`.
