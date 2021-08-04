import jsonlines
import json

curlist_old = []
with open("jarviz/jarviz-cli/result/output_old.jsonl", "r+", encoding="utf8") as f:
    for item in jsonlines.Reader(f):
        curlist_old.append(item)
with open("output_old.json", "w") as f:
    json.dump(curlist_old, f, ensure_ascii=False)

curlist_new = []
with open("jarviz/jarviz-cli/result/output_new.jsonl", "r+", encoding="utf8") as f:
    for item in jsonlines.Reader(f):
        curlist_new.append(item)
with open("output_new.json", "w") as f:
    json.dump(curlist_new, f, ensure_ascii=False)

