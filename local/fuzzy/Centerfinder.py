from math import *


def get_centerpoint(lis):
    area = 0.0
    x, y = 0.0, 0.0

    a = len(lis)
    for i in range(a):
        lng = lis[i][0]  # jingdu
        lat = lis[i][1]  # weidu

        if i == 0:
            lng1 = lis[-1][0]
            lat1 = lis[-1][1]

        else:
            lng1 = lis[i - 1][0]
            lat1= lis[i - 1][1]

        fg = (lat * lng1 - lng * lat1) / 2.0

        area += fg
        x += fg * (lat + lat1) / 3.0
        y += fg * (lng + lng1) / 3.0

    x = x / area
    y = y / area

    return x, y


def center_geolocation(geolocations):
    '''
    输入多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])，找出中心点
    :param geolocations:
    :return:中心点坐标  [lon,lat]
    '''
    # 求平均数  同时角度弧度转化 得到中心点
    x = 0  # lon
    y = 0  # lat
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        #  radians(float(lon))   Convert angle x from degrees to radians
        # 	                    把角度 x 从度数转化为 弧度
        lat = radians(float(lat))
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)
        x = float(x / lenth)
        y = float(y / lenth)
        z = float(z / lenth)
    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


# 得到离中心点里程最近的里程

def geodistance(lon1, lat1, lon2, lat2):
    '''
    得到两个经纬度坐标距离 单位为千米 （计算不分前后顺序）
    :param lon1: 第一个坐标 维度
    :param lat1: 第一个坐标 经度
    :param lon2: 第二个坐标 维度
    :param lat2: 第二个坐标 经度
    :return: distance 单位千米
    '''
    # lon1,lat1,lon2,lat2 = (120.12802999999997,30.28708,115.86572000000001,28.7427)
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])  # 经纬度转换成弧度
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    distance = 2 * asin(sqrt(a)) * 6371 * 1000  # 地球平均半径，6371km
    distance = round(distance / 1000, 3)
    return distance


def getMaxestDistance(geolocations, centre):
    '''
    中心点 距离 多个经纬度左边 最远的距离
    :param geolocations: 多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])
    :param centre: 中心点   centre [lon,lat]
    :return: 最远距离  千米
    '''
    distantces = []
    for lon, lat in geolocations:
        d = geodistance(lat, lon, centre[1], centre[0])
        distantces.append(d)
    return max(distantces)


def getOnePolyygen(geolocations):
    '''
    输入多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])，找出距该多边形中心点最远的距离
    :param geolocations:多个经纬度坐标(格式：[[lon1, lat1],[lon2, lat2],....[lonn, latn]])
    :return:center,neartDistance  多边形中心点  最远距离
    '''
    center = center_geolocation(geolocations)  # 得到中心点
    neartDistance = getMaxestDistance(geolocations, center)
    return center, neartDistance
