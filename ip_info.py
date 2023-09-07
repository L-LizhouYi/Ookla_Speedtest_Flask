import requests
from bisect import bisect_right

RESERVED_IPV4 = [
    '0.0.0.0/8',
    '10.0.0.0/8',
    '100.64.0.0/10',
    '127.0.0.0/8',
    '169.254.0.0/16',
    '172.16.0.0/12',
    '192.0.0.0/24',
    '192.0.2.0/24',
    '192.88.99.0/24',
    '192.168.0.0/16',
    '198.18.0.0/15',
    '198.51.100.0/24',
    '203.0.113.0/24',
    '224.0.0.0/4',
    '233.252.0.0/24',
    '240.0.0.0/4',
    '255.255.255.255/32'
]

API_URL = "http://ip-api.com/json/"


def ip2int(ip):
    return sum(int(p) << i for i, p in zip([24, 16, 8, 0], ip.split('.')))


def get_reserved_ranges():
    return [(ip2int(ip), ip2int(ip) + (1 << 32 >> int(m)) - 1) for rip in RESERVED_IPV4 for ip, m in [rip.split("/")]]


def is_reserved(ip):
    ip_ranges = get_reserved_ranges()
    ip_starts, ip_ends = zip(*sorted(ip_ranges))
    first_byte = {b for s, e in ip_ranges for b in range(s >> 24, (e >> 24) + 1)}
    if ip >> 24 not in first_byte:
        return False
    i = max(0, bisect_right(ip_starts, ip) - 1)
    return ip_starts[i] <= ip <= ip_ends[i]


def get_ip_info(ip):
    test_globals = {
        "ipAddress": "127.0.0.1",
        "ispName": "LocalHost",
        "ispId": 0,
        "location": {
            "latitude": 0,
            "longitude": 0,
            "cityName": "unknown",
            "countryCode": "unknown",
            "countryName": "unknown",
            "regionCode": "unknown",
            "regionName": "unknown"
        }
    }

    if is_reserved(ip2int(ip)):
        test_globals["ipAddress"] = ip
    else:
        try:
            response = requests.get(f"{API_URL}{ip}")
            if response.status_code == 200:
                res_json = response.json()
                location = test_globals["location"]
                location.update({
                    "latitude": res_json["lat"],
                    "longitude": res_json["lon"],
                    "cityName": res_json["city"],
                    "countryCode": res_json["countryCode"],
                    "countryName": res_json["country"],
                    "regionCode": res_json["region"],
                    "regionName": res_json["regionName"]
                })
                test_globals["ipAddress"] = res_json["query"]
                test_globals["ispName"] = res_json["isp"]
        except requests.RequestException as e:
            print(f"从API获取数据时出错：{e}")

    return test_globals


if __name__ == '__main__':
    a = is_reserved(ip2int('192.18.1.1'))
    print(a)