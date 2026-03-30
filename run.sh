#!/bin/bash
set -e

# Создать venv если нет
if [ ! -d ".venv" ]; then
    uv venv
    uv pip install groq
fi

# Запустить скрипт
.venv/bin/python3 ai.py
