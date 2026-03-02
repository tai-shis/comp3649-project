#!/usr/bin/env bash

echo "Running tests..."

python -m unittest -v tests.scanner_test
python -m unittest -v tests.parser_test
python -m unittest -v tests.instruction_buffer_test
python -m unittest -v tests.graph_test
python -m unittest -v tests.asm_generation_test
