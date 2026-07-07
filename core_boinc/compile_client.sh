#!/bin/bash
# Compilation script for the native C++ BOEINC client
set -e

CDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Compiling native C++ client..."
g++ -O3 -fopenmp -o "$CDIR/dark3_s12_sieve" "$CDIR/src/main.cpp"

echo "Native C++ client compiled successfully at $CDIR/dark3_s12_sieve!"
