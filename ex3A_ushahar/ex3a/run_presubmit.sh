#!/bin/bash

SCRIPT_PATH=$(realpath "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")
PYTHON_SCRIPT="$SCRIPT_DIR/run_presubmit.py"
EX_FOLDER="$SCRIPT_DIR/ex_info"
python3 "$PYTHON_SCRIPT" "$EX_FOLDER" $1
