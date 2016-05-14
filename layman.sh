#!/usr/bin/env bash
echo layman-script repl -v 0.1
echo -------------------------
while true; do
    read -p "> " input
    python main.py "$input"
done
