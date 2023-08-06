import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point,Polygon,shape,LineString
import urllib.request
import json
import CoordinatesConverter
from urllib import parse
from urllib import request

def getadmin(keyword,ak,subdistricts = False):
    '''
    Input the keyword and the Amap ak. The output is the GIS file of the administrative boundary (Only in China)
    
    Parameters
    -------
    keywords : str
        The keyword. It might be the city name such as Shengzheng, or the administrative code such as 440500
    ak : str
        Amap accesstoken
    subdistricts : bool
        Whether to output the information of the administrative district boundary

    Returns
    -------
    admin : GeoDataFrame
        Administrative district
    districts : DataFrame
        The information of subdistricts. This can be used to further get the boundary of lower level districts
    '''
    
    #查询的接口地址
    url = 'https://restapi.amap.com/v3/config/district?'
    #查询的条件
    dict1 = {
    'subdistrict':'3',
        'showbiz':'false',
        'extensions':'all',
        'key':ak,#这个是我的开发者key，告诉高德这个数据是我抓的，每天会有限额，你们可以注册成为开发者，这样就有自己的key拉
        's':'rsv3',
        'output':'json',
        'level':'district',
        'keywords':keyword,
        'platform':'JS',
        'logversion':'2.0',
        'sdkversion':'1.4.10'
    }
    #把查询条件组合成网页地址
    url_data = parse.urlencode(dict1)
    url = url+url_data
    #创建一个访问器
    request = urllib.request.Request(url)
    #访问网页
    response = urllib.request.urlopen(request)
    #读取网页内容
    webpage = response.read()
    #将内容用json解析
    result = json.loads(webpage.decode('utf8','ignore'))
    #读取整理数据
    datas = []
    k = 0
    polyline = result['districts'][k]['polyline']
    polyline1 = polyline.split('|')
    res = []
    for polyline2 in polyline1:
        polyline2 = polyline2.split(';')
        p = []
        for i in polyline2:
            a,b = i.split(',')
            p.append([float(a),float(b)])
        x = pd.DataFrame(p)
        x[0],x[1] = CoordinatesConverter.gcj02towgs84(x[0],x[1])
        p = x.values
        res.append(Polygon(p))
    data = pd.DataFrame()
    data1 = pd.DataFrame()
    data1['geometry'] = res
    data1 = gpd.GeoDataFrame(data1)
    poly = data1.unary_union
    data['geometry'] = [poly]
    try:
        data['citycode'] = result['districts'][k]['citycode']
    except:
        pass
    try:
        data['adcode'] = result['districts'][k]['adcode']
    except:
        pass
    try:
        data['name'] = result['districts'][k]['name']
    except:
        pass
    try:
        data['level'] = result['districts'][k]['level']
    except:
        pass
    try:
        data['center'] = result['districts'][k]['center']
    except:
        pass
    datas.append(data)
    datas = pd.concat(datas)
    admin = gpd.GeoDataFrame(datas)
    if subdistricts:
        districts = result['districts'][k]['districts']
        districts = pd.DataFrame(districts)
        return admin,districts
    else:
        return admin



def getbusdata(city,keywords):
    '''
    Obtain the geographic information of the bus station and bus line from the map service (Only in China)

    Parameters
    -------
    city : str
        city name
    keywords : List
        Keyword, the line name

    Returns
    -------
    data : GeoDataFrame
        The generated bus line
    stop : GeoDataFrame
        The generated bus station
    '''
    def getlineuid(keyword,c):
        url = 'http://map.baidu.com/?qt=s&wd='+urllib.parse.quote(keyword)+'&c='+c
        response1 = urllib.request.urlopen(url)
        searchinfo=json.loads(response1.read().decode('utf8'))
        if searchinfo['content'][0]['catalogID'] ==904 or searchinfo['content'][0]['catalogID'] ==905:
            try:
                uidlist = list(pd.DataFrame(searchinfo['content'][8]['blinfo'])['uid'])
            except:
                uidlist = []
            uidlist.append(searchinfo['content'][0]['uid'])
            uidlist.append(searchinfo['content'][1]['uid'])
            return list(set(uidlist))
        else:
            return []
    def getcitycode(c):
        url = 'http://map.baidu.com/?qt=s&wd='+urllib.parse.quote(c)
        response1 = urllib.request.urlopen(url,timeout = 60)
        searchinfo=json.loads(response1.read().decode('utf8'))
        return str(searchinfo['content']['code'])
    def getlinegeo(uid,c):
        url = 'http://map.baidu.com/?qt=bsl&uid='+uid+'&c='+c
        response = urllib.request.urlopen(url,timeout = 60)
        searchinfo=json.loads(response.read().decode('utf8'))
        linename = searchinfo['content'][0]['name']
        stations = searchinfo['content'][0]['stations']
        geo = searchinfo['content'][0]['geo'].split('|')[2][:-1].split(',')
        stationgeo = []
        stationnames = []
        for station in stations:
            stationname = station['name']
            coo = station['geo'].split(';')[1].split('|')[0]
            stationnames.append(stationname)
            stationgeo.append(coo)
        coo=[]
        t=0
        cood = ''
        for each in geo:
            t += 1
            cood += each + ','
            if t == 2:
                t=0
                coo.append(cood[:-1])
                cood = ''
        def coodconvert(coo):
            coo = pd.DataFrame(list(pd.DataFrame(coo)[0].str.split(','))).astype(float)
            coo[0],coo[1] = CoordinatesConverter.bd09mctobd09(coo[0],coo[1])
            return list(coo[0].astype(str)+','+coo[1].astype(str))
        return linename,coodconvert(coo),stationnames,coodconvert(stationgeo)
    print('Obtaining city id:',city,end = '')
    linenames = []
    lines = []
    c = getcitycode(city)
    print('success')
    stop = []
    uids = []
    
    for keyword in keywords:
        print(keyword)
        for uid in getlineuid(keyword,c):
            if uid not in uids:
                try:
                    linename,coo,stationnames,stationgeo = getlinegeo(uid,c)
                    coo = pd.DataFrame(list(pd.DataFrame(coo)[0].str.split(',')))
                    coo[0],coo[1] = CoordinatesConverter.bd09towgs84(coo[0],coo[1])
                    line = LineString(coo.values)
                    linenames.append(linename)
                    lines.append(line)
                    stops = pd.DataFrame({'stationnames':stationnames})
                    stops['linename']=linename
                    stops['geo'] = stationgeo
                    stops['lon'] = stops['geo'].apply(lambda row:row.split(',')[0])
                    stops['lat'] = stops['geo'].apply(lambda row:row.split(',')[1])
                    stop.append(stops)
                    print(linename+' success')
                    uids.append(uid)
                except:
                    pass
    data = gpd.GeoDataFrame()
    data['linename'] = linenames
    data['geometry'] = lines
    data['city'] = city
    stop = pd.concat(stop)
    stop['lon'],stop['lat'] = CoordinatesConverter.bd09towgs84(stop['lon'],stop['lat'])
    stop['geometry'] = gpd.points_from_xy(stop['lon'],stop['lat'])
    stop = stop.drop('geo',axis = 1)
    stop = gpd.GeoDataFrame(stop)
    data['line'] = data['linename'].str.split('(').apply(lambda r:r[0])
    stop['line'] = stop['linename'].str.split('(').apply(lambda r:r[0])
    stop['id'] = range(len(stop))
    stop['id'] = stop.groupby('linename')['id'].rank()
    data = data.drop_duplicates(subset = ['linename'])
    stop = stop.drop_duplicates(subset = ['linename','stationnames'])
    return data,stop

def split_subwayline(line,stop):
    '''
    To slice the metro line with metro stations to obtain metro section information (This step is useful in subway passenger flow visualization)

    Parameters
    -------
    line : GeoDataFrame
        Bus/metro lines
    stop : GeoDataFrame
        Bus/metro stations

    Returns
    -------
    metro_line_splited : GeoDataFrame
        Generated section line shape
    '''
    def getline(r2,line_geometry):
        #生成空的list用以存放轨道断面的节点
        ls = []
        #对大部分情况，线段的起点的位置在终点前，在起终点之间生成10个点
        if r2['o_project']<=r2['d_project']:
            #numpy的linespace线性插值生成10个点距离线段起点的距离
            tmp1 = np.linspace(r2['o_project'],r2['d_project'],10)
        #对四号线环线，最后一个站点与第一个站点之间的轨道断面需要特殊处理
        if r2['o_project']>r2['d_project']:
            tmp1 = np.linspace(r2['o_project']-line_geometry.length,r2['d_project'],10)
            tmp1[tmp1<0] = tmp1[tmp1<0]+line_geometry.length
        #tmp1存储的是点距离线段起点的距离，将每个距离转换为点要素，并添加到ls中
        for j in tmp1:
            ls.append(line_geometry.interpolate(j))
        #最后，把点序列转换为线型输出
        return LineString(ls)
    lss = []
    #遍历每条轨道线
    for k in range(len(line)):
        r = line.iloc[k]
        #获取轨道线的线型
        line_geometry = r['geometry']
        #提取相应的站点
        tmp = stop[stop['linename'] == r['linename']].copy()
        #生成轨道段
        for i in tmp.columns:
            tmp[i+'1'] = tmp[i].shift(-1)
        tmp = tmp.iloc[:-1]
        tmp = tmp[['stationnames','stationnames1','geometry','geometry1','linename']]
        #提取轨道段起终点在线路上对应的位置
        tmp['o_project'] = tmp['geometry'].apply(lambda r1:r['geometry'].project(r1))
        tmp['d_project'] = tmp['geometry1'].apply(lambda r1:r['geometry'].project(r1))
        #遍历提取轨道段
        tmp['geometry'] = tmp.apply(lambda r2:getline(r2,line_geometry),axis = 1)
        #提取的轨道段放进list中
        lss.append(tmp)
    #遍历完后，合并list里的表，得到轨道断面信息表
    metro_line_splited = pd.concat(lss).drop('geometry1',axis = 1)
    #绘制轨道断面
    return metro_line_splited


def metro_network(stop,traveltime = 3,transfertime = 5,nxgraph = True):
    '''
    Inputting the metro station data and outputting the network topology model. The graph generated relies on NetworkX.

    Parameters
    -------
    stop : GeoDataFrame
        Bus/metro stations
    traveltime : number
        Travel time per section
    transfertime : number
        Travel time per transfer
    nxgraph : bool
        Default True, if True then output the network G constructed by NetworkX, if False then output the edges1(line section),edge2(station transfer), and the node of the network

    Returns
    -------
    G : networkx.classes.graph.Graph
        Network G built by networkx. Output when the nxgraph parameter is True
    edge1 : DataFrame
        Network edge for line section. Output when the nxgraph parameter is False
    edge2 : DataFrame
        Network edge for transfering. Output when the nxgraph parameter is False
    node : List
        Network nodes. Output when the nxgraph parameter is False
    '''
    linestop = stop.copy()
    #提取相邻站点够成的轨道段
    for i in linestop.columns:
        linestop[i+'1'] = linestop[i].shift(-1)
    linestop = linestop[linestop['linename'] == linestop['linename1']].copy()
    #重命名列名
    linestop = linestop.rename(columns = {'stationnames':'ostop','stationnames1':'dstop'})
    #构建站点名称，使得不同线路不同站点能够区分
    linestop['ostation'] = linestop['line']+linestop['ostop']
    linestop['dstation'] = linestop['line']+linestop['dstop']
    #构建网络边的第一部分：即轨道段形成的边
    edge1 = linestop[['ostation','dstation']].copy()
    #假定地铁搭一个站点耗时3分钟
    edge1['duration'] = traveltime
    #读取轨道站点数据
    linestop = stop.copy()
    linestop['station'] = linestop['line'] + linestop['stationnames']
    #提取出换乘站
    tmp = linestop.groupby(['stationnames'])['linename'].count().rename('count').reset_index()
    tmp = pd.merge(linestop,tmp[tmp['count']>2]['stationnames'],on = 'stationnames')
    #为换乘站构建边
    tmp = tmp[['stationnames','line','station']].drop_duplicates()
    tmp = pd.merge(tmp,tmp,on ='stationnames')
    #提取换乘边，假定换乘耗时为5分钟
    edge2 =tmp[tmp['line_x'] != tmp['line_y']][['station_x','station_y']]
    edge2['duration'] = transfertime
    edge2.columns = edge1.columns
    #将两类边合体
    edge = edge1.append(edge2)
    #提取其中的节点
    node = list(edge['ostation'].drop_duplicates())
    if nxgraph:
        #构建轨道网络
        import networkx as nx
        #先创建一个空网络
        G = nx.Graph()
        #添加节点
        G.add_nodes_from(node)
        #添加含有权重的无向边
        G.add_weighted_edges_from(edge.values)
        return G
    else:
        return edge1,edge2,node

