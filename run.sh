#!/bin/sh

# get the two method mapping files
cd jarviz/jarviz-cli
./jarviz output_old -f setting/filter.json -a setting/artifacts_old.json
./jarviz output_new -f setting/filter.json -a setting/artifacts_new.json
cd ../..

# change the output form
python3 jsonl_to_json.py

# show the UI
python3 JsonTreeView/treeview.py