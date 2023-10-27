from flask import Blueprint, render_template,request,redirect,url_for,jsonify,current_app
from app.modules.db_utils import Speedtest
from app.modules.ip_info import *
from app.config import *

app_views = Blueprint('app_views', __name__)

# 初始化数据库
ObjSpeedtest = Speedtest()

# 根路由
@app_views.route('/')
def index():
    client_ip = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
    data_ip = get_ip_info(client_ip)
    return render_template(TEMPLATE_NAME, data_ip=data_ip, data_rep=None)

# 返回Speedtest Server
@app_views.route('/api/js/servers', methods=['GET'])
def get_json_datas():
    limit = request.args.get('limit')
    search = request.args.get('search', None)
    engine = request.args.get('engine', None)

    if engine != None:
        objData = ObjSpeedtest.get_servers(limit=limit, search_engine=engine)

    else:
        objData = ObjSpeedtest.get_servers(limit=limit, search_engine=search)

    ServerList = [i for i in objData]
    return jsonify(ServerList)


# 测速完成，用于接收数据
@app_views.route('/report', methods=['POST'])
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
        current_app.logger.error(f"Error while adding speedtest log: {str(e)}")
        return redirect(url_for('app_views.index'))


# 根据 result_guid 获取历史记录
@app_views.route('/result/<string:result_guid>')
def get_history(result_guid):
    client_ip = request.headers.get('X-Forwarded-For', request.headers.get('X-Real-IP', request.remote_addr))
    data_ip = get_ip_info(client_ip)
    try:
        history_data = ObjSpeedtest.get_speedtest_log(result_guid)
        return render_template(TEMPLATE_NAME, data_ip=data_ip, data_rep=history_data)
    except Exception as e:
        # 处理数据库查询异常
        current_app.logger.error(f"Error while fetching speedtest history: {str(e)}")
        return redirect(url_for('app_views.index'))
