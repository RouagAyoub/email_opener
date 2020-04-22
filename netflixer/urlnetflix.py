from selenium import webdriver
import time

username = 'dadzdadazdazdadadazdazd@gma.co'
password = 'fb_password'

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
else:
    print('no')
#time.sleep(3)
#driver.close()
