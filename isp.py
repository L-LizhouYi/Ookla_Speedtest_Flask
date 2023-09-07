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


def ip2int(ip):
    return sum(int(p) << i for i, p in zip([24, 16, 8, 0], ip.split('.')))


ipRanges = [(ip2int(ip), ip2int(ip) + (1 << 32 >> int(m)) - 1)
            for rip in RESERVED_IPV4 for ip, m in [rip.split("/")]]
ipStarts, ipEnds = zip(*sorted(ipRanges))
firstByte = {b for s, e in ipRanges for b in range(s >> 24, (e >> 24) + 1)}


def isReserved(ip):
    if ip >> 24 not in firstByte: return False
    i = max(0, bisect_right(ipStarts, ip) - 1)
    return ipStarts[i] <= ip <= ipEnds[i]


# 模板数据
testGlobals = {
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


def get_ip_info(ip):
    if isReserved(ip2int(ip)):
        testGlobals["ipAddress"] = ip
    else:
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}")
            if response.status_code == 200:
                resJosn = response.json()
                testGlobals["ipAddress"] = resJosn["query"]
                testGlobals["ispName"] = resJosn["isp"]
                testGlobals["location"]["latitude"] = resJosn["lat"]
                testGlobals["location"]["longitude"] = resJosn["lon"]
                testGlobals["location"]["cityName"] = resJosn["city"]
                testGlobals["location"]["countryCode"] = resJosn["countryCode"]
                testGlobals["location"]["countryName"] = resJosn["country"]
                testGlobals["location"]["regionCode"] = resJosn["region"]
                testGlobals["location"]["regionName"] = resJosn["regionName"]

        except:
            pass

    return testGlobals


if __name__ == '__main__':
    # a = get_ip_info("8.8.8.8")
    # print(a)
    a = isReserved(ip2int('192.18.1.1'))
    print(a)
