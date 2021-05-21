from bs4 import BeautifulSoup
from epcdata.login_zabbix import *
import requests
import re

mme_host = {'MME21':'10691','MME22':'10727','MME23':'10692','MME24':'10728','MME25':'10986',
            'MME26':'10987','MME27':'10988','MME06':'10765','MME08':'10745','MME0C':'10928'}
#saegw_host = {'SAEGW0A':'10902'}
cmg_host = {'SAEGW2A':'10974','SAEGW2B':'10975','SAEGW2C':'10991','SAEGW2D':'10976',
            'SAEGW2E':'10977','SAEGW2F':'10992','SAEGW0C':'10961','SAEGW0E':'10998','SAEGW0F':'11008','SAEGW0G':'11001'}
cmg_7850 = {'SAEGW2A_IB1':'10978','SAEGW2A_IB2':'10979','SAEGW2B_IB1':'10980','SAEGW2B_IB2':'10981','SAEGW2C_IB1':'10993','SAEGW2C_IB2':'10994',
            'SAEGW2D_IB1':'10982','SAEGW2D_IB2':'10983', 'SAEGW2E_IB1':'10984','SAEGW2E_IB2':'10985', 'SAEGW2F_IB1':'10995','SAEGW2F_IB2':'10996',
            'SAEGW0C_IB1':'10952','SAEGW0C_IB2':'10953','SAEGW0E_IB1':'11002','SAEGW0E_IB2':'11003','SAEGW0F_IB1':'11004','SAEGW0F_IB2':'11005',
            'SAEGW0G_IB1':'11006','SAEGW0G_IB2':'11007'}
fw_host = {'FW21':'10723','FW22':'10724','FW23':'10716','FW24':'10715','FW03':'10721','FW04':'10722',
           'FW65':'11030','FW66':'11031','FW67':'11032','FW68':'11033'}
fw_5g_host={'FW25':'11054','FW26':'11055','FW27':'11058','FW28':'11059','FW29':'11056','FW2A':'11057'}
host_group = {'nsn_mme':'31','nsn_saegw':'40','nsn_cmg':'56','cmg_7850':'57','hw_fw':'16','fw_5g_host':'66'}
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
         'Host':'10.209.11.4'}

def get_mme_data(session,mme,refer=''):
    global headers
    mmedata={}
    dict = requests.utils.dict_from_cookiejar(session.cookies)
    sid = dict['zbx_sessionid'][16:]
    url = 'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['nsn_mme'],mme,sid)
    #print(url)
    headers['Refer'] = refer
    r = session.get(url, headers=headers)

    soup=BeautifulSoup(r.text,'lxml')
    regex=re.compile('.*Total')
    x = soup.find('td',text=regex).find_next_sibling().find_next_sibling().text
    mmedata['enbnum'] = int(x)
    regex = re.compile('.*calEPS_ATTACH_SUCC_Rate')
    x = soup.find('td',text=regex).find_next_sibling().find_next_sibling().text
    mmedata['attasucceratio'] = float(x)
    regex = re.compile('.*extAttached_User_2G_Sum')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    if int(x)>2200000:
        mmedata['num2g']=0
    else:
        mmedata['num2g'] = int(x)
    regex = re.compile('.*extAttached_User_4G_Sum_31225')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    regex = re.compile('.*extAttached_User_4G_Sum_36263')
    x1 = soup.find('td', text=regex)
    if x1 is not None:
        num = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
        if int(num) > 100000:
            x = num
    mmedata['num4g'] = int(x)
    print(mmedata)
    return mmedata


def get_ng_data(session,saegw):
    global headers
    saegwdata = {}
    dict = requests.utils.dict_from_cookiejar(session.cookies)
    sid = dict['zbx_sessionid'][16:]
    url =  'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['nsn_saegw'],saegw,sid)
    #headers['Refer'] = refer
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    regex = re.compile(r'.*THROUGHT_OCTETS_Sgi_SUM')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    v=x[:-5]
    if x[-4:] == 'Gbps':
        saegwdata['sgiflow'] = float(v)
    elif x[-4:] == 'Mbps':
        saegwdata['sgiflow'] = round(float(v) / 1024,2)
    else:
        saegwdata['sgiflow'] = 0
    regex = re.compile(r'.*extSessionsRatEutranActiveNum_SUM')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    saegwdata['session4g'] = int(x)
    regex = re.compile(r'.*extSessionsRatGeranActiveNum_SUM')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    saegwdata['session2g'] = int(x)
    print(saegwdata)
    return saegwdata

def get_cmg_data(session,cmg):
    global headers
    cmgdata = {}
    dict = requests.utils.dict_from_cookiejar(session.cookies)
    sid = dict['zbx_sessionid'][16:]
    url = 'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['nsn_cmg'], cmg, sid)
    # headers['Refer'] = refer
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    regex = re.compile(r'.*PGW PDN Sessions\(2\/3G\) in Total')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    cmgdata['session2g'] = int(x)
    regex = re.compile(r'.*PGW PDN Sessions\(LTE\) in Total')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    cmgdata['session4g'] = int(x)
    host_cmg = {v:k for k,v in cmg_host.items()}
    url = 'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['cmg_7850'], cmg_7850[host_cmg[cmg]+'_IB1'], sid)
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    regex = re.compile(r'.*InterfacesGroup_Throughput_Gi$')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    v = x[:-5]
    if x[-4:] == 'Gbps':
        tmp = float(v)
    elif x[-4:] == 'Mbps':
        tmp = round(float(v) / 1024, 2)
    else:
        tmp = 0
    cmgdata['sgiflow'] = tmp
    url = 'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['cmg_7850'], cmg_7850[host_cmg[cmg] + '_IB2'], sid)
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    regex = re.compile(r'.*InterfacesGroup_Throughput_Gi$')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    v = x[:-5]
    if x[-4:] == 'Gbps':
        tmp1 = float(v)
    elif x[-4:] == 'Mbps':
        tmp1 = round(float(v) / 1024, 2)
    else:
        tmp1 = 0
    if tmp1>cmgdata['sgiflow']:
        cmgdata['sgiflow']=tmp1
    cmgdata['sgiflow']=round(cmgdata['sgiflow'],2)
    print(cmgdata)
    return cmgdata


def get_fw_data(session,fw):
    global headers
    fwdata = {}
    dict = requests.utils.dict_from_cookiejar(session.cookies)
    sid = dict['zbx_sessionid'][16:]
    if fw in fw_host.values():
        url = 'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['hw_fw'], fw, sid)
    elif fw in fw_5g_host.values():
        url = 'http://10.209.11.4/zabbix/latest.php?open=1&groupid=%s&hostid=%s&select=&sid=%s' % (host_group['fw_5g_host'], fw, sid)
    r = session.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    regex = re.compile('.*extTotalSessionCurrently')
    x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
    fwdata['sessionnum'] = int(x)
    for i in range(1,5):
        if (fw==fw_host['FW21'] or fw==fw_host['FW22'] or fw==fw_host['FW65'] or fw==fw_host['FW66'] or fw==fw_host['FW67']
            or fw==fw_host['FW68'] or fw==fw_5g_host['FW29'] or fw==fw_5g_host['FW2A']) and i == 4:
            fwdata['trunk' + str(i) + 'flow'] =0
            break;
        regex = re.compile('.*extIfInVolume_Eth_Trunk'+str(i))
        x = soup.find('td', text=regex).find_next_sibling().find_next_sibling().text
        v = x[:-5]
        if x[-4:] == 'Gbps':
            fwdata['trunk'+str(i)+'flow'] = float(v)
        elif x[-4:] == 'Mbps':
            fwdata['trunk'+str(i)+'flow'] = round(float(v) / 1024,2)
        else:
            fwdata['trunk'+str(i)+'flow'] = 0
    print(fwdata)
    return fwdata

def test(url='https://www.baidu.com'):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': '10.209.11.4'}
    session = requests.session()
    r = session.get(url, headers=headers)
    #print(r.text)
    soup = BeautifulSoup(r.text, 'lxml')
    regex = re.compile('.*extAttached_User_4G_Sum_36263')
    x1 = soup.find('s1cript')
    if x1 is not None:
        print('123')

if  __name__  ==  '__main__':


    s=login_zabbix('zhuolun','zhuolun')

    for fw in fw_host:
        print(fw)
        get_fw_data(s, fw_host[fw])






