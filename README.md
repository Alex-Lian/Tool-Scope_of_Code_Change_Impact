# 无端科技 版本修改可视化工具

## 文件结构
1. jarviz           (文件夹)     生成method调用关系
2. JsonTreeView     (文件夹)     生成可视化界面
3. run.sh           (执行脚本)
4. jsonl_to_json.py (python脚本) 文件格式转换
5. input.txt        (文档)       业务入口的输入

## 环境要求
python3, java, maven
python包: jsonlines, PyQt5

## 使用流程
1. 把新旧两个版本的jar包 放入 `jarviz/jarviz-cli/input-jar` 中， 并分别命名为 `new-0.0.0.jar` 和 `old-0.0.0.jar`
2. 将需要的业务入口方法名填入 `input.txt` 
3. 执行脚本 `sh run.sh`

