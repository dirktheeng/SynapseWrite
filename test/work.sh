#!/bin/bash
# Deterministic work count (edges, visits, lazy reads, pull evaluations) for each benchmark event.
clang -DCOUNT --target=wasm32 -O3 -nostdlib -mbulk-memory -msimd128 -Wl,--no-entry -Wl,-z,stack-size=1048576 -o build/engine_count.wasm host/engine.c
ENGINE=build/engine_count.wasm node test/bench.js 2>/dev/null | grep work | sed 's/  */ /g'
