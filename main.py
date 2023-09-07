from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    from ip_info import get_ip_info
    client_ip = request.remote_addr
    data = get_ip_info(client_ip)
    return render_template('index.html', data=data)


# 返回Speedtest Server
@app.route('/api/js/servers')
def get_json_datas():
    from speedtest_servers import serverList
    data = serverList
    return jsonify(data)

# 测速完成 用于接收数据, 目前是个摆设 但是前端会传
@app.route('/report',methods=['POST'])
def post_report_data():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
