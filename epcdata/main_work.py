from epcdata.login_zabbix import *
from epcdata.epc_database import *
from epcdata.collect_data import *
from datetime import datetime
import time,threading

Key = True
def main_work():
    global Key
    num=0
    key0 = True
    while Key:
        try:
            now = datetime.now().strftime('%M')
            t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if (now == '05' or now == '15' or now == '25' or now == '35' or now == '45' or now == '55') and key0:
                key0 = False
                s = login_zabbix('zhuolun', 'zhuolun')
                s_database = get_mysql_session()
                for mme in mme_host:
                    print(mme)
                    md=get_mme_data(s, mme_host[mme])
                    mmedata=MmeData(entity_name=mme,enb_num=md['enbnum'],atta_2g_num=md['num2g'],atta_4g_num=md['num4g'], atta_success_ratio=md['attasucceratio'],date_time=t)
                    s_database.add(mmedata)
                    s_database.commit()
                '''    
                for saegw in saegw_host:
                    print(saegw)
                    sd=get_ng_data(s, saegw_host[saegw])
                    saegwdata=SaegwData(entity_name=saegw,sgi_flow =sd['sgiflow'],session_2g_num=sd['session2g'],session_4g_num=sd['session4g'],date_time=t)
                    s_database.add(saegwdata)
                    s_database.commit()
                '''
                for cmg in cmg_host:
                    print(cmg)
                    cd=get_cmg_data(s, cmg_host[cmg])
                    cmgdata=SaegwData(entity_name=cmg,sgi_flow =cd['sgiflow'],session_2g_num=cd['session2g'],session_4g_num=cd['session4g'],date_time=t)
                    s_database.add(cmgdata)
                    s_database.commit()
                for fw in fw_host:
                    print(fw)
                    fd=get_fw_data(s, fw_host[fw])
                    fwdata=FwData(entity_name=fw,session_num =fd['sessionnum'],trunk1_in_flow =fd['trunk1flow'],trunk2_in_flow =fd['trunk2flow'],trunk3_in_flow =fd['trunk3flow'],trunk4_in_flow =fd['trunk4flow'],date_time =t)
                    s_database.add(fwdata)
                    s_database.commit()
                for fw in fw_5g_host:
                    print(fw)
                    fd = get_fw_data(s, fw_5g_host[fw])
                    fwdata = FwData(entity_name=fw, session_num=fd['sessionnum'], trunk1_in_flow=fd['trunk1flow'],
                                    trunk2_in_flow=fd['trunk2flow'], trunk3_in_flow=fd['trunk3flow'],
                                    trunk4_in_flow=fd['trunk4flow'], date_time=t)
                    s_database.add(fwdata)
                    s_database.commit()
                logout_zabbix(s)
                s_database.close()
            if not (now == '05' or now == '15' or now == '25' or now == '35' or now == '45' or now == '55'):
                key0 = True
            time.sleep(5)
        except:
            time.sleep(5)
            logout_zabbix(s)
            s_database.close()
            num+=1
            print('采集程序出现异常'+str(num)+'次')

if __name__ == '__main__':

    workthread = threading.Thread(target=main_work)
    workthread.start()

    #global Key

    while True:
        s = input('input start or stop?')
        if s =='stop':
            Key=False
            print('采集程序已经终止')
            break
