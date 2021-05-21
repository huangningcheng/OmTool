import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime,timedelta

# saegw_host = ['SAEGW21','SAEGW22','SAEGW23','SAEGW27','SAEGW04','SAEGW05','SAEGW06','SAEGW08','SAEGW0A']


def is_realtime_data_lost():
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.30:3306/epc_data?charset=utf8", echo=True)
    sdate = (pd.datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    fw_sql = 'select * from fw_data where date_time > ' + '\'' + sdate + '\' and (entity_name=\'FW04\' or entity_name=\'FW22\' or entity_name=\'FW24\')'
    df = pd.read_sql(fw_sql, engine)
    latesttime = df.tail(1).reset_index(drop=True)['date_time'][0]
    diffminiute = (pd.datetime.now() - latesttime).total_seconds() / 60
    if diffminiute > 20:
        return True
    else:
        return False


def sae_kpi_monito(date=0):
    # df = pd.read_excel('data/saegw_data.xlsx', date_parser='date_time')

    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.30:3306/epc_data?charset=utf8", echo=True)
    sdate = (pd.datetime.now()-timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    sae_sql = 'select * from saegw_data where date_time > '+ '\''+sdate + '\''
    df = pd.read_sql(sae_sql, engine)
    latesttime = df.tail(1).reset_index(drop=True)['date_time'][0]
    ldate = latesttime.strftime('%Y-%m-%d %H:%M')
    df = df.set_index('date_time')
    dflatest = df[ldate].drop('id',axis=1)
    delta = timedelta(days=1)
    histime = latesttime - delta
    hdate = histime.strftime('%Y-%m-%d %H:%M')
    dfhis = df[hdate].drop('id',axis=1)
    while dfhis.shape[0] == 0:
        histime = histime - delta
        hdate = histime.strftime('%Y-%m-%d %H:%M')
        dfhis = df[hdate].drop('id', axis=1)
    rp = ''
    for i in range(dflatest.shape[0]):
        if dfhis.iloc[i]['entity_name'] == dflatest.iloc[i]['entity_name']:
            s = round(100*(dflatest.iloc[i]['sgi_flow'] - dfhis.iloc[i]['sgi_flow'])/dfhis.iloc[i]['sgi_flow'],2)
            if s < -10 and dfhis.iloc[i]['entity_name'] != 'SAEGW2E':
                rp = rp + dfhis.iloc[i]['entity_name'] + ' sgi flow changed:%s'%s+'% \n'
            s = round(100 * (dflatest.iloc[i]['session_4g_num'] - dfhis.iloc[i]['session_4g_num']) / dfhis.iloc[i]['session_4g_num'], 2)
            if s < -10 and dfhis.iloc[i]['entity_name'] != 'SAEGW2E':
                rp = rp + dfhis.iloc[i]['entity_name'] +' session_4g_num change:%s'%s+'% \n'
    return rp


def mme_kpi_monito(date=0):
    # df = pd.read_excel('data/mme_data.xlsx', date_parser='date_time')
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.30:3306/epc_data?charset=utf8", echo=True)
    sdate = (pd.datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    mme_sql = 'select * from mme_data where date_time > ' + '\''+sdate + '\''
    df = pd.read_sql(mme_sql, engine)
    latesttime = df.tail(1).reset_index(drop=True)['date_time'][0]
    ldate = latesttime.strftime('%Y-%m-%d %H:%M')
    df = df.set_index('date_time')
    dflatest = df[ldate].drop('id',axis=1)
    delta = timedelta(days=1)
    histime = latesttime - delta
    hdate = histime.strftime('%Y-%m-%d %H:%M')
    dfhis = df[hdate].drop('id',axis=1)
    while dfhis.shape[0] == 0:
        histime = histime - delta
        hdate = histime.strftime('%Y-%m-%d %H:%M')
        dfhis = df[hdate].drop('id', axis=1)
    rp = ''
    for i in range(dflatest.shape[0]):
        if dfhis.iloc[i]['entity_name'] == dflatest.iloc[i]['entity_name']:
            s = dflatest.iloc[i]['enb_num'] - dfhis.iloc[i]['enb_num']
            if s < -50:
                rp = rp + dfhis.iloc[i]['entity_name'] + ' enb lost more than:%s'%-s+'\n'
            s = round(100 * (dflatest.iloc[i]['atta_4g_num'] - dfhis.iloc[i]['atta_4g_num']) / dfhis.iloc[i]['atta_4g_num'], 2)
            if s < -5:
                rp = rp + dfhis.iloc[i]['entity_name'] +' atta_4g_num change:%s'%s+'% \n'
            s = dflatest.iloc[i]['atta_success_ratio'] - dfhis.iloc[i]['atta_success_ratio']
            if s < -10:
                rp = rp + dfhis.iloc[i]['entity_name'] + ' atta_success_ratio reduce:%s' % -s + '% \n'
    return rp

def fw_kpi_monito(date=0):
    # df = pd.read_excel('data/fw_data.xlsx', date_parser='date_time')
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.30:3306/epc_data?charset=utf8", echo=True)
    sdate = (pd.datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    fw_sql = 'select * from fw_data where date_time > ' + '\''+sdate + '\' and (entity_name=\'FW04\' or entity_name=\'FW22\' or entity_name=\'FW24\')'
    df = pd.read_sql(fw_sql, engine)
    latesttime = df.tail(1).reset_index(drop=True)['date_time'][0]
    ldate = latesttime.strftime('%Y-%m-%d %H:%M')
    df = df.set_index('date_time')
    dflatest = df[ldate].drop('id', axis=1)
    delta = timedelta(days=1)
    histime = latesttime - delta
    hdate = histime.strftime('%Y-%m-%d %H:%M')
    dfhis = df[hdate].drop('id', axis=1)
    while dfhis.shape[0] == 0:
        histime = histime - delta
        hdate = histime.strftime('%Y-%m-%d %H:%M')
        dfhis = df[hdate].drop('id', axis=1)
    rp = ''
    for i in range(dflatest.shape[0]):
        if dfhis.iloc[i]['entity_name'] == dflatest.iloc[i]['entity_name']:
            s = round(100 * (dflatest.iloc[i]['session_num'] - dfhis.iloc[i]['session_num']) / dfhis.iloc[i]['session_num'], 2)
            if s < -10:
                rp = rp + dfhis.iloc[i]['entity_name'] + ' session_num changed:%s' % s + '% \n'
            s = round(100 * (dflatest.iloc[i]['trunk1_in_flow'] - dfhis.iloc[i]['trunk1_in_flow']) / dfhis.iloc[i][
                'trunk1_in_flow'], 2)
            if s < -10:
                rp = rp + dfhis.iloc[i]['entity_name'] + ' Gi Flow change:%s' % s + '% \n'
    return rp


'''
df = pd.read_excel('data/saegw_data.xlsx',date_parser='date_time')
#saegw2d_data = df.loc[(df['entity_name'] == 'SAEGW2D') ].set_index('date_time').truncate(before='2019-10-07 00:00:00')
saegw2d_data = df.loc[(df['entity_name'] == 'SAEGW2D')].tail(1).reset_index(drop=True)
delta = timedelta(days=1)
print(saegw2d_data['date_time'][0].strftime('%Y-%m-%d %H:%M'))
print((saegw2d_data['date_time'][0]-delta).strftime('%Y-%m-%d %H:%M'))


saegw2d_data = df.loc[(df['entity_name'] == 'SAEGW2D') ].set_index('date_time')
print(saegw2d_data['2019-10-07 00:15'].shape[1])
'''

if __name__ == '__main__':
    #rs = is_realtime_data_lost()
    sdate = '2019-11-27 00:00:00'
    fw_sql = 'select * from fw_data where date_time > ' + '\'' + sdate + '\' and (entity_name=\'FW04\' or entity_name=\'FW22\' or entity_name=\'FW24\')'
    print(fw_sql)
    a='123'
    b= '456'+a+'789'
    print(b)
    b = '456 a 789'
    print(b)

