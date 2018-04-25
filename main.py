import json
import os
import re
import sys
import uuid
from string import Template

from flask import Flask, jsonify, request

import conf_parse

API_V1 = '/api/v1/'
app = Flask(__name__, static_url_path='')

memo = Template("""
###### $tip #######
""")


# 加载静态资源html
@app.route("/")
def index():
    return app.send_static_file('index.html')


# 加载已添加的规则
def load_rule():
    with open(sys.path[0] + 'new/add.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)
    return rules


# 保存规则到json
def save_rule(rules_json):
    with open(sys.path[0] + 'new/add.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(rules_json, ensure_ascii=False, indent=4))


# 将规则的json文件中的提取并转化成str
def change_json2str(_rules):
    naxsi_core = ''
    naxsi = ''
    for k, v in _rules.items():
        naxsi_core += '{0}{1}\n'.format(memo.substitute(tip=v['title']), v['naxsi_core'])
        naxsi += v['naxsi'] + '\n'
    return naxsi_core, naxsi


# 将规则的json文件中的信息并转化成list
def json2list():
    rules = load_rule()
    results = []
    for k, v in rules.items():
        results.append({"uuid": k, "title": v["title"], "naxsi_core": v["naxsi_core"], "naxsi": v["naxsi_core"]})
    return results


# 添加的规则列表
@app.route(API_V1 + "rules", methods=['GET'])
def list_rules():
    return jsonify(rules=json2list())


# 修改防护地址
@app.route(API_V1 + "modify", methods=['POST'])
def modify_url():
    data = json.loads(str(request.data, encoding='utf-8'))
    url = data['url']
    status = '-1'
    if re.match(r'^https?:/{2}\w.+$', url):
        conf_parse.update_conf(url)
        os.system('nginx -s reload')
        status = '0'
        message = '成功'
    else:
        message = '地址不合法'
    result = {"status": status, "message": message}
    return jsonify(result)


# 更新规则
@app.route(API_V1 + "update", methods=['POST'])
def update_rule():
    status = '-1'
    try:
        data = json.loads(str(request.data, encoding='utf-8'))
        rules = load_rule()
        if data['uuid'] in rules.keys():
            rules[data['uuid']]['naxsi_core'] = data['naxsi_core']
            rules[data['uuid']]['naxsi'] = data['naxsi']
            save_rule(rules)
            result = change_json2str(rules)
            conf_parse.add_rule2file(result[0], result[1])
            # 重启容器[docker restart $(docker ps -q)]/重启nginx [nginx -s reload]
            os.system('nginx -s reload')
            status = '0'
            message = '成功'
        else:
            message = '没有此规则，无法更新'
    except Exception as e:
        print(e)
        message = '处理异常，失败'
    result = {"status": status, "message": message}
    return jsonify(result)


# 添加规则
@app.route(API_V1 + 'add', methods=['POST'])
def add_rule():
    try:
        rules = load_rule()
        data = json.loads(str(request.data, encoding='utf-8'))
        rules[str(uuid.uuid1())] = data
        save_rule(rules)
        result = change_json2str(rules)
        conf_parse.add_rule2file(result[0], result[1])
        # 重启容器[docker restart $(docker ps -q)]/重启nginx [nginx -s reload]
        os.system('nginx -s reload')
        return jsonify({"status": "0", "message": "成功"})
    except Exception as e:
        print(e)
        return jsonify({"status": "-1", "message": "处理异常，失败"})


# 编辑规则
@app.route(API_V1 + 'edit', methods=['POST'])
def edit_rule():
    try:
        rules = load_rule()
        data = json.loads(str(request.data, encoding='utf-8'))
        rules[data['uuid']] = data['data']
        save_rule(rules)
        result = change_json2str(rules)
        conf_parse.add_rule2file(result[0], result[1])
        # 重启容器[docker restart $(docker ps -q)]/重启nginx [nginx -s reload]
        os.system('nginx -s reload')
        return {"status": "0", "message": "成功"}
    except:
        return {"status": "-1", "message": "处理异常，失败"}


# 根据id获取规则
@app.route(API_V1 + 'get/<uuid_>', methods=['GET'])
def get_rule(uuid_):
    rules = load_rule()
    result = rules[uuid_]
    return jsonify(result)


# 获取防护地址
@app.route(API_V1 + 'getURL', methods=['GET'])
def get_url():
    return jsonify(url=conf_parse.get_conf())


# 删除规则
@app.route(API_V1 + 'removeRule', methods=['POST'])
def remove_rule():
    try:
        data = json.loads(request.data)
        rules = load_rule()
        rules.pop(data['uuid'])
        save_rule(rules)
        result = change_json2str(rules)
        conf_parse.add_rule2file(result[0], result[1])
        return jsonify({"status": "0", "message": "成功"})
    except:
        return jsonify({"status": "-1", "message": "处理异常，失败"})


if __name__ == '__main__':
    os.system('nginx -g daemon off;')
    app.run(host='0.0.0.0', debug=False, threaded=True)
