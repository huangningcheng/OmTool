from datetime import datetime
import time,threading
from data_monito.kpi_monito import *
from data_monito.mail_process import *

rev_list = ['huangningcheng@139.com','18850567199@139.com','13696993653@139.com','13779977163@139.com',
            '13606019596@139.com','13950196668@139.com','18850313986@139.com']
Key = True
def main_work():
    #print(saegw_host)
    global Key
    num=0
    while Key:
        try:
            now = datetime.now().strftime('%M')
            sec = datetime.now().strftime('%S')
            t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if now == '00' or now == '10' or now == '20' or now == '30' or now == '40' or now == '50':
                if int(sec) < 10:
                    if is_realtime_data_lost():
                        mail = mail_util('zhiji', 'Asdf.2k3', 'smtp.fj.chinamobile.com')
                        mail.mail_send(rev_list, 'EPC实时监控数据丢失' + t, s)
                    else:
                        s = ''
                        s = mme_kpi_monito()
                        s = s + sae_kpi_monito()
                        s = s + fw_kpi_monito()
                        if s != '' and rev_list != []:
                            mail = mail_util('zhiji', 'Asdf.2k3','smtp.fj.chinamobile.com')
                            mail.mail_send(rev_list, 'EPC实时监控警报'+t, s)
                    time.sleep(10)

            time.sleep(5)
            #print('hello')
        except Exception as e:
            print (e)
            time.sleep(5)

            num+=1
            print('监控程序出现异常'+str(num)+'次')

def interac_active():
    global Key
    global rev_list
    while Key:
        hour = datetime.now().strftime('%H')
        if hour == '08':
            rev_list = ['huangningcheng@139.com', '18850567199@139.com', '13696993653@139.com', '13779977163@139.com',
                        '13606019596@139.com', '13950196668@139.com', '18850313986@139.com']
        mail = mail_util('zhiji','Asdf.2k3','smtp.fj.chinamobile.com')
        mail_top3 = mail.mail_rev()
        for mail_info in mail_top3:
            if mail_info['Subject'].find('EPC实时监控警报') != -1:
                time = re.findall(r'\d.+', mail_info['Subject'])[0]
                alarm_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                d = alarm_time.strftime('%d')
                h = alarm_time.strftime('%H')
                cmd = mail_info['Content'].split()[0]
                word = mail_info['Content'].split()[1]+'@139.com'
                if d == datetime.now().strftime('%d') and h == datetime.now().strftime('%H'):
                    if cmd == 'stop':
                        if word in rev_list:
                            rev_list.remove(word)
                    if cmd == 'add':
                        if word not in rev_list:
                            rev_list.add(word)
                    mail.mail_del(mail_info['index'])
        time.sleep(60)


if __name__ == '__main__':
    workthread = threading.Thread(target=main_work)
    workthread.start()
    interac_thread = threading.Thread(target=interac_active)
    interac_thread.start()

    # global Key

    while True:
        s = input('input start or stop?')
        if s == 'stop':
            Key = False
            print('监控程序已经终止')
            break
