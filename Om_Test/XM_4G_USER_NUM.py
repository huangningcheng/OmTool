import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime

def show_xm_4G_user(sdate,edate=0):
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    #sdate = pd.datetime.now().strftime('%Y-%m-%d ') + '10:35:0_'
    # sql = 'select DATE_FORMAT(date_time,\'%%m-%%d\') date,round(sum(atta_4g_num)/10000,1) num_4g from mme_data where entity_name like \'MME2_\' and date_time like ' + '\'2020-__-__ 11:35:__\' ' \
    #     'and date_time > \'2020-04-28 00:00:00\' group by date_time'
    if edate == 0:
        edate = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        edate = pd.to_datetime(edate, format='%Y%m%d')
        edate = datetime.datetime.strftime(edate, '%Y-%m-%d %H:%M:%S')
    sdate = pd.to_datetime(sdate, format='%Y%m%d')
    sdate = datetime.datetime.strftime(sdate, '%Y-%m-%d %H:%M:%S')
    sql = 'select DATE_FORMAT(date_time,\'%%m-%%d\') date,ROUND(sum(atta_4g_num)/10000) num_4g from mme_data where entity_name like \'MME2_\' and date_time like ' + '\'202_-__-__ 11:35:__\' ' \
        'and date_time >= \''+sdate+'\''+'and date_time <= \''+edate+'\''+' group by date_time'
    print(sql)
    df = pd.read_sql(sql, engine)
    #df.to_excel("ATTAUSER.xls",index=None)
    # rs = pd.datetime.now().strftime('%Y-%m-%d ') + '厦门MME附着用户数' + str(round(df['num_4g'][0] / 10000, 1)) + '万'
    tick_label = list(df['date'])
    y = list(df['num_4g'])
    recs = plt.bar(tick_label, y)

    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x() + rec.get_width() / 2, h, int(h), ha='center', va='bottom')
    plt.xticks(rotation=-90)
    plt.title("厦门4G附着用户数（单位：万）")
    plt.show()

def show_xm_2G_user(sdate,edate=0):
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    #sdate = pd.datetime.now().strftime('%Y-%m-%d ') + '10:35:0_'
    # sql = 'select DATE_FORMAT(date_time,\'%%m-%%d\') date,round(sum(atta_4g_num)/10000,1) num_4g from mme_data where entity_name like \'MME2_\' and date_time like ' + '\'2020-__-__ 11:35:__\' ' \
    #     'and date_time > \'2020-04-28 00:00:00\' group by date_time'
    if edate == 0:
        edate = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        edate = pd.to_datetime(edate, format='%Y%m%d')
        edate = datetime.datetime.strftime(edate, '%Y-%m-%d %H:%M:%S')
    sdate = pd.to_datetime(sdate, format='%Y%m%d')
    sdate = datetime.datetime.strftime(sdate, '%Y-%m-%d %H:%M:%S')
    sql = 'select DATE_FORMAT(date_time,\'%%m-%%d\') date,ROUND(sum(atta_2g_num)/10000) num_4g from mme_data where entity_name like \'MME2_\' and date_time like ' + '\'202_-__-__ 11:35:__\' ' \
        'and date_time >= \''+sdate+'\''+'and date_time <= \''+edate+'\''+' group by date_time'
    print(sql)
    df = pd.read_sql(sql, engine)
    #df.to_excel("ATTAUSER.xls",index=None)
    # rs = pd.datetime.now().strftime('%Y-%m-%d ') + '厦门MME附着用户数' + str(round(df['num_4g'][0] / 10000, 1)) + '万'
    tick_label = list(df['date'])
    y = list(df['num_4g'])
    recs = plt.bar(tick_label, y)

    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x() + rec.get_width() / 2, h, int(h), ha='center', va='bottom')
    plt.xticks(rotation=-90)
    plt.title("厦门2G附着用户数（单位：万）")
    plt.show()


if __name__=='__main__':
    #show_xm_4G_user('20210301','20210401')
   show_xm_4G_user('20210501')
   show_xm_2G_user('20210501')
