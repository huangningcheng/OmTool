import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

def decode_str(s):
    value, charset = decode_header(s)[0]
    #print(charset)
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

pop3_server = 'pop3.fj.chinamobile.com'
server = poplib.POP3(pop3_server)
#server.set_debuglevel(1)
server.user('zhiji@fj.chinamobile.com')
server.pass_('Asdf.2k3')
resp, mails, octets = server.list()

index = len(mails)
for i in range(1):
    resp, lines, octets = server.retr(index-i)
    #print(type(lines))
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    msg = Parser().parsestr(msg_content)
    value = msg.get('Subject', '')
    s = decode_str(value)
    print(s)
    value = msg.get('From','')
    s = decode_str(value)
    print(s)
    if msg.is_multipart():
        print('msg is multipart')
        parts = msg.get_payload()
        part=parts[0]
        if not part.is_multipart():
            content_type = part.get_content_type()
            print(content_type)
            charset = guess_charset(part)
            print(charset)
            content = part.get_payload(decode=True)
            content = content.decode(charset)
            print(content)
    else:
        print('msg is not multipart')
        content_type = msg.get_content_type()
        print(content_type)
        charset = guess_charset(msg)
        print(charset)
        content = msg.get_payload(decode=True)
        content = content.decode(charset)
        print(content)
server.quit()