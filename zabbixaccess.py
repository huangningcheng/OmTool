'''
接入zabbix系统
'''
import requests
from requests_toolbelt import MultipartEncoder

m=MultipartEncoder(fields={'form_refresh':'1','form':'1','name':'zhuolun','password':'zhuolun','enter':'Enter'},boundary='----WebKitFormBoundaryB7xziwZQ3bnAFVLY')

url='http://10.209.11.4/zabbix/index.php?login=1'
headers={'content-type':'multipart/form-data; boundary=----WebKitFormBoundaryB7xziwZQ3bnAFVLY','User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}
s=requests.session()
r=s.post(url,data=m,headers=headers,allow_redirects=True)
print(r.text)
print(type(r.cookies))
dict=requests.utils.dict_from_cookiejar(r.cookies)
sid=dict['zbx_sessionid'][16:]
print(len(list(sid)))
#url='http://10.209.11.4/zabbix/latest.php?open=1&applicationid=1586&groupid=31&hostid=10691&fullscreen=0&select=enb&sid='+sid
url='http://10.209.11.4/zabbix/latest.php?open=1&applicationid=1586&groupid=31&hostid=10691&fullscreen=0&select=enb'
print(url)
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
         'Host':'10.209.11.4'}
r=s.get(url,headers=headers)
print(r.text)
#print(r.cookies)