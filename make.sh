#!/bin/bash
# Build everything: engine, weights, page. Run from anywhere.
set -e
cd "$(dirname "$0")"; mkdir -p build
clang --target=wasm32 -O3 -nostdlib -mbulk-memory -msimd128 -Wl,--no-entry -Wl,-z,stack-size=1048576 -o build/engine.wasm host/engine.c
(cd gen && python3 app.py)
python3 build.py
