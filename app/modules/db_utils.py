from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from .sqlite_server import SpeedtestServer,SpeedtestHistory,engine,Base
class Speedtest:
    def __init__(self):
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()

    def __del__(self):
        self.session.close()

    # 从数据库中获取服务器
    def get_servers(self, limit, search_engine):
        try:
            query = self.session.query(SpeedtestServer)
            if search_engine != "js":
                query = query.filter(SpeedtestServer.sponsor.like(f"%{search_engine}%"))

            server_records = query.limit(limit).all()
            return [
                {
                    "id": server.id,
                    "sponsor": server.sponsor,
                    "name": server.name,
                    "host": server.host,
                    "url": server.url,
                    "country": server.country,
                    "cc": server.cc,
                    "lat": server.lat,
                    "lon": server.lon,
                    "distance": server.distance,
                    "preferred": server.preferred,
                    "https_functional": server.https_functional,
                    "force_ping_select": server.force_ping_select,
                    "show": server.show,
                    "internal": server.internal
                }
                for server in server_records
            ]
        except OperationalError:
            Base.metadata.create_all(engine)
            return []

    # 通过id获取单个服务器信息
    def get_server_info(self, id):
        result = self.session.query(SpeedtestServer).filter_by(id=id).first()
        result = {
            "serverSponsor": result.sponsor,
            "serverName": result.name
        }
        return result

    # 添加测速记录
    def add_speedtest_log(self, data):
        ''' data 数据格式
        {
            "ispName": "39.87.54.3",
            "serverSponsor": "湖南联通5G（官方）",
            "serverName": "长沙",
            "serverId": 0,
            "jitter": 47.888888888888886,
            "latency": 36,
            "upload": 5699375,
            "download": 1319375,
            "guid": "0938c990-4d90-11ee-a138-3d1d9426b53e"
        }
        '''

        speedtest_history = SpeedtestHistory(**data)
        self.session.add(speedtest_history)
        self.session.commit()

    # 获取测速记录
    def get_speedtest_log(self, guid):
        result = self.session.query(SpeedtestHistory).filter_by(guid=guid).first()
        result = {
            "ispName": result.ispName,
            "serverSponsor": result.serverSponsor,
            "serverName": result.serverName,
            "serverId": result.serverId,
            "jitter": result.jitter,
            "latency": result.latency,
            "upload": result.upload,
            "download": result.download,
            "guid": result.guid,
            "resultDate": result.resultDate.strftime('%Y-%m-%d %H:%M:%S')
        }
        return result
