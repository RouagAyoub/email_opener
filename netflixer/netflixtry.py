import email
import imaplib

username = 'maybeemee90@gmail.com'
password = 'Sr1iz49$'
url = 'imap.gmail.com'


def getbody(msg):
    if msg.is_multipart():
        return getbody(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def search(key, value, con):
    resul, data = con.search(None, key, '"{}"'.format(value))
    return data

def get_email(result_bytes):
    msgs=[]
    for num in result_bytes[0].split():
        typ, data =con.fetch(num, '(RFC822)')
        msgs.append(data)
    return msgs
    


#def connexion(n):
    #up = n.split(':')


con = imaplib.IMAP4_SSL(url)
con.login(username, password)
con.select('INBOX')
result, data = con.fetch(b'3','RFC822')
raw = email.message_from_bytes(data[0][1])
print(getbody(raw))


#def main():
    #with open('file name','w',encoding='utf-8') as file1:
     #   newlist = list(file1)
      #  for n in list:
            #connexion('maybeemee90@gmail.com:Sr1iz49$')

            

#if __name__ == '__main__':
    #main()