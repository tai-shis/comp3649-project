#!/usr/bin/env bash

echo "Running tests..."

python -m unittest -v tests.token_test
python -m unittest -v tests.scanner_test
python -m unittest -v tests.parser_test
python -m unittest -v tests.instruction_test
python -m unittest -v tests.instruction_buffer_test
python -m unittest -v tests.liveness_test
python -m unittest -v tests.interference_graph_test
python -m unittest -v tests.asm_instruction_test
python -m unittest -v tests.asm_generation_test