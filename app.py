from flask import Flask, jsonify, render_template, request, redirect, url_for
from modules.ip_info import get_ip_info
from modules.sqlite_server import Speedtest

app = Flask(__name__)
app.config['STATIC_URL_PATH'] = '/static'
TEMPLATE_NAME = 'index.html'

# 初始化数据库
ObjSpeedtest = Speedtest()

# 根路由
@app.route('/')
def index():
    client_ip = request.remote_addr
    data_ip = get_ip_info(client_ip)
    return render_template(TEMPLATE_NAME, data_ip=data_ip, data_rep=None)

# 处理 404 错误的函数
@app.errorhandler(404)
def not_found(error):
    return redirect(url_for('index'))  # 重定向到根路径


# 返回Speedtest Server
@app.route('/api/js/servers')
def get_json_datas():
    objData = ObjSpeedtest.get_servers()
    ServerList = [i for i in objData]
    return jsonify(ServerList)


# 测速完成，用于接收数据
@app.route('/report', methods=['POST'])
def post_report_data():
    form_data = request.form.to_dict()
    ispName = form_data.get('clientip')
    serverId = form_data.get('serverid')

    jitter = form_data.get('jitter')
    latency = form_data.get('ping')
    upload = form_data.get('upload')
    download = form_data.get('download')
    guid = form_data.get('guid')

    server_info = ObjSpeedtest.get_server_info(serverId)
    serverSponsor = server_info.get('serverSponsor')
    serverName = server_info.get('serverName')

    data = {
        "ispName": ispName,
        "serverSponsor": serverSponsor,
        "serverName": serverName,
        "serverId": serverId,
        "jitter": jitter,
        "latency": latency,
        "upload": int(upload) * 125,
        "download": int(download) * 125,
        "guid": guid
    }
    try:
        ObjSpeedtest.add_speedtest_log(data)
        return jsonify({"resultid": guid})
    except Exception as e:
        # 处理数据库操作异常
        app.logger.error(f"Error while adding speedtest log: {str(e)}")
        return redirect(url_for('index'))


# 根据 result_guid 获取历史记录
@app.route('/result/<string:result_guid>')
def get_history(result_guid):
    client_ip = request.remote_addr
    data_ip = get_ip_info(client_ip)
    try:
        history_data = ObjSpeedtest.get_speedtest_log(result_guid)
        return render_template(TEMPLATE_NAME, data_ip=data_ip, data_rep=history_data)
    except Exception as e:
        # 处理数据库查询异常
        app.logger.error(f"Error while fetching speedtest history: {str(e)}")
        return redirect(url_for('index'))


# 启动应用
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
