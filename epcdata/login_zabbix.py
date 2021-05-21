'''
接入zabbix系统
'''
import requests
import hashlib
import base64
from requests_toolbelt import MultipartEncoder

def str2hex_str(data):
    res=''
    for s in data:
        res += hex(ord(s))[2:]
    return res.upper()

def login_zabbix(username,passwd):
    #username = str2hex_str(username)
    #passwd = str2hex_str(passwd)
    #m = MultipartEncoder(fields={'form_refresh': str2hex_str('1'), 'form': str2hex_str('1'), 'name':username, 'password': passwd, 'enter': str2hex_str('Enter')},boundary='----WebKitFormBoundaryB7xziwZQ3bnAFVLY')
    m = MultipartEncoder(
        fields={'form_refresh': '1', 'form': '1', 'name': username, 'password': passwd,
                'enter': 'Enter'}, boundary='----WebKitFormBoundaryB7xziwZQ3bnAFVLY')
    url = 'http://10.209.11.4/zabbix/index.php?login=1'
    headers = {'content-type': 'multipart/form-data; boundary=----WebKitFormBoundaryB7xziwZQ3bnAFVLY',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    session = requests.session()
    session.post(url, data=m, headers=headers, allow_redirects=True)
    dict = requests.utils.dict_from_cookiejar(session.cookies)
    sid = dict['zbx_sessionid'][16:]
    url = 'http://10.209.11.4/zabbix/latest.php?sid=%s&filter_rst=1'%sid
    #print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Host': '10.209.11.4'}
    session.get(url, headers=headers)
    return session
'''
    dict = requests.utils.dict_from_cookiejar(session.cookies)
    sid = dict['zbx_sessionid'][16:]
    data={}
    data['sid'] = sid
    data['form_refresh'] = '1'
    data['form'] = '1'
    data['select'] = ''
    data['filter_set'] = 'Filter'
    url='http://10.209.11.4/zabbix/latest.php'
    session.post(url, data=data, headers=headers, allow_redirects=True)
'''




def logout_zabbix(session):
    url = 'http://10.209.11.4//zabbix/index.php?reconnect=1'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
    session.get(url, headers=headers)


if __name__ == '__main__':
    session=login_zabbix('zhuolun','zhuolun')

   # dict = requests.utils.dict_from_cookiejar(session.cookies)
   # sid = dict['zbx_sessionid'][16:]
   # url = 'http://10.209.11.4/zabbix/latest.php?open=1&applicationid=1586&groupid=31&hostid=10691&fullscreen=0&select=enb&sid=' + sid
    #url = 'http://10.209.11.4/zabbix/latest.php?open=1&applicationid=1586&groupid=31&hostid=10691&fullscreen=0&select=enb'
    #print(url)
    #headers = {
    #    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    #    'Host': '10.209.11.4'}
    #r = session.get(url, headers=headers)
    #print(r.text)
    pwd = '1'
    print(str2hex_str(pwd))