#!/bin/bash

echo "Welcome to use Bisheng Test Module"

nginx
uvicorn --host 0.0.0.0 --workers 2 --port 5250 tests.gradio_app.app:app
