#!/usr/bin/env python

import sys
import csv
import argparse
from datetime import datetime
import hashlib
import re
import requests


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--refresh-token', nargs='?', dest="refresh_token",
                        type=str, required=True, help='refresh token')
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help='csv file containing alb logs from tiles.rasterfoundry.com')

    args = parser.parse_args()

    token = requests.post(
        "https://app.rasterfoundry.com/api/tokens/",
        json={"refresh_token": args.refresh_token},
    ).json()["id_token"]

    url_matcher = re.compile(".+\.com(:\d{1,})?\/(.+)")
    token_matcher = re.compile("(\?|&)token=(.+)")
    project_id_matcher = re.compile(
        "2ff937c2-1efd-40d1-8ef1-84fabf1cd25f\/(.+)")
    reader = csv.reader(args.input_file, delimiter=',')

    # Skip headers
    next(reader)
    for row in reader:
        creation = datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S.%f %Z")
        nano_seconds = int(creation.timestamp() * 1000000000)
        request_url = row[3]

        # Some requests in the ALB logs don't conform
        if not url_matcher.match(request_url):
            continue

        path = url_matcher.split(request_url)[-2]
        path = token_matcher.sub("\\1token=" + token, path)

        if project_id_matcher.match(path):
            path = project_id_matcher.sub(
                "a50adc14-95c3-4159-90a3-6fde0c37667b/\\1", path)

        if path.startswith('2c7abeda-145f-421f-9417-f2785b530200') or path.startswith('8cf57be8-0d6a-49bf-8c79-f49ae4a0eaf7'):
            continue

        request = (
            "1 {} {}\n".format(hashlib.sha1(
                path.encode("utf-8")).hexdigest(), nano_seconds),
            "GET /{} HTTP/1.1\n".format(path),
            "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36\n",
            "Accept-Encoding: gzip\n",
            "Host: tiles.rasterfoundry.com\n",
            "Connection: close\n",
            "\n\n🐵🙈🙉"
        )

        print(''.join(request))


if __name__ == "__main__":
    main()
