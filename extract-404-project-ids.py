import re

req_ids = []
req_id_matcher = re.compile("\d (.+) \d+ \d+\n")
initial_req_id_matcher = re.compile("1 (.+) \d+")
project_id_matcher = re.compile("GET \/(.+)\/\d+\/\d+\/\d+\/.+")

project_ids = []

with open("responses_0.log", "rb") as lines:
    last_line = ""
    for line in lines:
        try:
            line = line.decode("utf-8")

            if line.startswith("HTTP/2.0 404") and req_id_matcher.match(last_line):
                req_ids.append(req_id_matcher.search(last_line).group(1))
            last_line = line
        except:
            continue

with open("responses_0.log", "rb") as lines:
    get_this_line = False

    for line in lines:
        try:
            line = line.decode("utf-8")

            if get_this_line:
                project_ids.append(project_id_matcher.search(line).group(1))

            if not initial_req_id_matcher.match(line):
                get_this_line = False
                continue

            found_match = False

            for req_id in req_ids:
                if req_id in line:
                    get_this_line = True
                    found_match = True
                    break

            if not found_match:
                get_this_line = False
        except:
            continue

print(list(set(project_ids)))
