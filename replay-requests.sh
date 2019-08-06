#!/bin/bash

gor \
    --input-file "${1}|100%" \
    --output-http "https://tiles.rasterfoundry.com" \
    --output-http-stats \
    --output-http-track-response \
    --output-http-compatibility-mode \
    --stats \
    --output-file "responses.log" \
    --output-file-size-limit 256m \
    --output-file-queue-limit 0 \
    --output-http-workers-min 10
    # --output-http-debug \
    # --verbose \
    # --debug verbose