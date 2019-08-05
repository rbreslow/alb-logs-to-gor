#!/bin/bash

gor \
    --input-file "${1}|1000%" \
    --output-http "https://tiles.rasterfoundry.com" \
    --output-http-stats \
    --output-http-track-response \
    --output-http-compatibility-mode \
    --stats \
    --output-file "responses.log" \
    --output-http-workers 0 \
    --output-http-workers-min 10
    # --output-http-debug \
    # --verbose \
    # --debug verbose