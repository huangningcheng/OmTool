from email.mime.text import MIMEText
from email.header import Header
import smtplib
import poplib
from email.parser import Parser
from email.header import decode_header
import re
from datetime import datetime


class mail_util():
    def __init__(self,user,passwd,server):
        self.user = user
        self.passwd = passwd
        self.server = server

    def mail_send(self,to_list,title,content):
        server = smtplib.SMTP(self.server,25)
        #server.set_debuglevel(1)
        from_addr = self.user+'@fj.chinamobile.com'
        server.login(from_addr,self.passwd)
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = Header(from_addr, 'utf-8')
        msg['Subject'] = Header(title, 'utf-8').encode()
        server.sendmail(from_addr, to_list, msg.as_string())
        server.quit()

    def decode_str(self,s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def guess_charset(self,msg):
        charset = msg.get_charset()
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def mail_rev(self):
        pop3_server = 'pop3.fj.chinamobile.com'
        server = poplib.POP3(pop3_server)
        server.user(self.user+'@fj.chinamobile.com')
        server.pass_(self.passwd)
        resp, mails, octets = server.list()
        mail_list=[]
        index = len(mails)
        if index > 6:
            num = 6
        else:
            num = index
        for i in range(num):
            mail_info = {}
            mail_info['index'] = index - i
            resp, lines, octets = server.retr(index - i)
            msg_content = b'\r\n'.join(lines).decode('utf-8')
            msg = Parser().parsestr(msg_content)
            value = msg.get('Subject', '')
            mail_info['Subject'] = self.decode_str(value)
            value = msg.get('From', '')
            mail_info['From'] = self.decode_str(value)
            if msg.is_multipart():
                # print('msg is multipart')
                parts = msg.get_payload()
                part = parts[0]
                if not part.is_multipart():
                    content_type = part.get_content_type()
                    # print(content_type)
                    charset = self.guess_charset(part)
                    # print(charset)
                    content = part.get_payload(decode=True)
                    mail_info['Content'] = content.decode(charset)
            else:
                # print('msg is not multipart')
                content_type = msg.get_content_type()
                # print(content_type)
                charset = self.guess_charset(msg)
                # print(charset)
                content = msg.get_payload(decode=True)
                mail_info['Content'] = content.decode(charset)
                # print(content)
            mail_list.append(mail_info)
        server.quit()
        return mail_list

    def mail_del(self,index):
        pop3_server = 'pop3.fj.chinamobile.com'
        server = poplib.POP3(pop3_server)
        server.user(self.user + '@fj.chinamobile.com')
        server.pass_(self.passwd)
        server.dele(index)
        server.quit()


if __name__ == '__main__':
    mail = mail_util('zhiji','Asdf.2k3','smtp.fj.chinamobile.com')
    # mail.mail_send(['zhiji@fj.chinamobile.com'],'hello','this is text')
    rs = mail.mail_rev()
    if rs[0]['Subject'].find('EPC实时监控警报') != -1:
        print('true')
        print(rs[0]['Subject'])
        time = re.findall(r'\d.+',rs[0]['Subject'])[0]
        time = datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
        print(time.strftime('%d'))
    print(rs[0]['Content'].split()[1])
    print(rs[0])
    print(rs[1])
    print(rs[2])
    print(rs[3])
    #mail.mail_del(rs[0]['index'])
    #mail.mail_del(rs[1]['index'])
    #mail.mail_del(rs[2]['index'])


