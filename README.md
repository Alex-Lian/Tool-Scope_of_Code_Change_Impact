util for version compare

## File Structure
1. jarviz           (folder)     get the method dependency
2. JsonTreeView     (folder)     generate the version interface
3. run.sh           (shell script)
4. jsonl_to_json.py (python script) change the form of the file 
5. input.txt        (file)       defined first layer input

## Environment Requirement
python3, java, maven                    
python package: jsonlines, PyQt5

## How To Use It
1. put the old and new jar files to `jarviz/jarviz-cli/input-jar` and rename them to `new-0.0.0.jar`, `old-0.0.0.jar`
2. define the first layer input and put them to `input.txt` 
3. run `sh run.sh`

