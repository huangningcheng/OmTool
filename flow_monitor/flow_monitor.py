import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime
from matplotlib.pyplot import MultipleLocator
def init():
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

def fw_flow_view(start_time,end_time = 0,fw = 'FW04'):
    init()
    y_major_locator = MultipleLocator(10)
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,trunk1_in_flow,date_time from fw_data where entity_name=\''+fw+'\''+\
          ' and date_time >= \''+start_time+'\' and date_time <= \''+ end_time+'\''
    #print(sql)
    df = pd.read_sql(sql, engine)
    #quiretime = df['date_time'].apply(lambda x:x.strftime('%Y%m%d%H'))
    #print(quiretime)
    plt.plot(df['date_time'],df['trunk1_in_flow'])
    xd = []
    xl = []
    i = 0
    #print(df['date_time'])
    xd.append(df['date_time'][0])
    xl.append(df['date_time'][0].strftime('%m-%d'))

    for xdate in df['date_time']:
        if i%6 == 0:
            #print(xdate)
            xd.append(xdate)
            if i%144 == 0:
                xl.append(xdate.strftime('%m-%d'))
            else:
                xl.append(xdate.strftime('%H'))
        i +=1
    plt.xticks(xd,xl)
    plt.xticks(rotation=-90,fontsize=7)
    plt.title(fw+"实时吞吐量（单位：Gbps）")
    plt.grid(linestyle=":")
    if df['trunk1_in_flow'].max()>100:
        ax = plt.gca()
        ax.yaxis.set_major_locator(y_major_locator)
        #把y轴刻度设置为间隔10
    plt.show()

def mme_plt_attaratio_view(start_time,end_time = 0,mme = 'MME21'):
    init()
    y_major_locator = MultipleLocator(10)
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,atta_success_ratio,date_time from mme_data where entity_name=\''+mme+'\''+\
          ' and date_time >= \''+start_time+'\' and date_time <= \''+ end_time+'\''
    #print(sql)
    df = pd.read_sql(sql, engine)
    #quiretime = df['date_time'].apply(lambda x:x.strftime('%Y%m%d%H'))
    #print(quiretime)
    plt.plot(df['date_time'],df['atta_success_ratio'])
    xd = []
    xl = []
    i = 0
    #print(df['date_time'])
    xd.append(df['date_time'][0])
    xl.append(df['date_time'][0].strftime('%m-%d'))

    for xdate in df['date_time']:
        if i%6 == 0:
            #print(xdate)
            xd.append(xdate)
            if i%144 == 0:
                xl.append(xdate.strftime('%m-%d'))
            else:
                xl.append(xdate.strftime('%H'))
        i +=1
    plt.xticks(xd,xl)
    plt.xticks(rotation=-90,fontsize=7)
    plt.title(mme+"实时attach成功率（单位：%）")
    plt.grid(linestyle=":")
    plt.show()


def mme_plt_attauser_view(start_time,end_time = 0,mme = 'MME21'):
    init()
    y_major_locator = MultipleLocator(10)
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,atta_4g_num,date_time from mme_data where entity_name=\''+mme+'\''+\
          ' and date_time >= \''+start_time+'\' and date_time <= \''+ end_time+'\''
    #print(sql)
    df = pd.read_sql(sql, engine)
    #quiretime = df['date_time'].apply(lambda x:x.strftime('%Y%m%d%H'))
    #print(quiretime)
    plt.plot(df['date_time'],df['atta_4g_num'])
    xd = []
    xl = []
    i = 0
    #print(df['date_time'])
    xd.append(df['date_time'][0])
    xl.append(df['date_time'][0].strftime('%m-%d'))

    for xdate in df['date_time']:
        if i%6 == 0:
            #print(xdate)
            xd.append(xdate)
            if i%144 == 0:
                xl.append(xdate.strftime('%m-%d'))
            else:
                xl.append(xdate.strftime('%H'))
        i +=1
    plt.xticks(xd,xl)
    plt.xticks(rotation=-90,fontsize=7)
    plt.title(mme+"实时附着用户数")
    plt.grid(linestyle=":")
    plt.show()

def xm_plt_attauser_view(start_time,end_time = 0):
    init()
    y_major_locator = MultipleLocator(10)
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,ROUND(sum(atta_4g_num)/10000) num_4g,date_time from mme_data where entity_name like \'MME2_\'and date_time >='+ '\''+start_time+\
          '\' and date_time <= \''+ end_time+'\''+' group by date_time'
    #print(sql)
    df = pd.read_sql(sql, engine)
    #quiretime = df['date_time'].apply(lambda x:x.strftime('%Y%m%d%H'))
    #print(quiretime)
    plt.plot(df['date_time'],df['num_4g'])
    xd = []
    xl = []
    i = 0
    #print(df['date_time'])
    xd.append(df['date_time'][0])
    xl.append(df['date_time'][0].strftime('%m-%d'))

    for xdate in df['date_time']:
        if i%6 == 0:
            #print(xdate)
            xd.append(xdate)
            if i%144 == 0:
                xl.append(xdate.strftime('%m-%d'))
            else:
                xl.append(xdate.strftime('%H'))
        i +=1
    plt.xticks(xd,xl)
    plt.xticks(rotation=-90,fontsize=7)
    plt.title("厦门MME实时附着用户数")
    plt.grid(linestyle=":")
    plt.show()

def saegw_flow_view(start_time,end_time = 0,saegw = 'SAEGW2A'):
    init()
    y_major_locator = MultipleLocator(10)
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,sgi_flow,date_time from saegw_data where entity_name=\''+saegw+'\''+\
          ' and date_time >= \''+start_time+'\' and date_time <= \''+ end_time+'\''
    #print(sql)
    df = pd.read_sql(sql, engine)
    #quiretime = df['date_time'].apply(lambda x:x.strftime('%Y%m%d%H'))
    #print(quiretime)
    plt.plot(df['date_time'],df['sgi_flow'])
    xd = []
    xl = []
    i = 0
    #print(df['date_time'])
    xd.append(df['date_time'][0])
    xl.append(df['date_time'][0].strftime('%m-%d'))

    for xdate in df['date_time']:
        if i%6 == 0:
            #print(xdate)
            xd.append(xdate)
            if i%144 == 0:
                xl.append(xdate.strftime('%m-%d'))
            else:
                xl.append(xdate.strftime('%H'))
        i +=1
    plt.xticks(xd,xl)
    plt.xticks(rotation=-90,fontsize=7)
    plt.title(saegw+"实时流量(单位：GB)")
    plt.grid(linestyle=":")
    plt.show()

def saegw_sessionnum_view(start_time,end_time = 0,saegw = 'SAEGW2A'):
    init()
    y_major_locator = MultipleLocator(10)
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,session_4g_num,date_time from saegw_data where entity_name=\''+saegw+'\''+\
          ' and date_time >= \''+start_time+'\' and date_time <= \''+ end_time+'\''
    #print(sql)
    df = pd.read_sql(sql, engine)
    #quiretime = df['date_time'].apply(lambda x:x.strftime('%Y%m%d%H'))
    #print(quiretime)
    plt.plot(df['date_time'],df['session_4g_num'])
    xd = []
    xl = []
    i = 0
    #print(df['date_time'])
    xd.append(df['date_time'][0])
    xl.append(df['date_time'][0].strftime('%m-%d'))

    for xdate in df['date_time']:
        if i%6 == 0:
            #print(xdate)
            xd.append(xdate)
            if i%144 == 0:
                xl.append(xdate.strftime('%m-%d'))
            else:
                xl.append(xdate.strftime('%H'))
        i +=1
    plt.xticks(xd,xl)
    plt.xticks(rotation=-90,fontsize=7)
    plt.title(saegw+" 4G会话数")
    plt.grid(linestyle=":")
    plt.show()

if __name__ == '__main__':
    fw_flow_view('20210501',fw='FW25')
    #mme_plt_attaratio_view('20210501',mme='MME21')
    #mme_plt_attauser_view('20210401', mme='MME27')
    #saegw_flow_view('20210401', saegw='SAEGW2A')
    #saegw_flow_view('20210401', saegw='SAEGW0C')
    #saegw_sessionnum_view('20210410',saegw='SAEGW2A')
    #xm_plt_attauser_view('20210401')
