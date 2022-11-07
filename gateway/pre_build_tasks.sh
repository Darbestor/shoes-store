#!/bin/bash
cd "$(dirname "$0")"
poetry export --without-hashes --output requirements.txt