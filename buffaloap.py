#!/usr/bin/env python3

# HCL
# WSR-2533DHP Version 1.06

# Usage:
# buffaloap.py [enable / enableall / disable / disableall]

import sys
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.firefox.options import Options

url = 'http://buffaloap.rio.st/login.html'

limited = [
	'0c:7a:15:0e:ed:c2', #Aoi's Chromebook
	'b0:19:c6:4a:f6:59', #AoiPhoneX
	'fc:65:de:d2:ed:83', #Kindle8
	'b8:78:26:40:16:32', #Switch
	'98:41:5c:dc:c3:ff' #SwitchLite
]

unlimited = [
	'70:ee:50:13:1a:1a', #NetAtmo
	'80:e6:50:12:c0:48', #MBPW???
	'38:f9:d3:3c:95:e0', #MacMiniW
	'f4:0f:24:2d:8b:c5', #MBP2016W
	'8c:85:90:9b:e8:07', #MBP2017W
	'f0:18:98:7b:fd:4d', #MBA2018W
	'e4:e4:ab:4f:3c:b4', #RioPhoneSE
	'f0:27:2d:78:82:99', #Kindle7
	'38:71:de:03:60:94', #YuiPhone6
	'4c:56:9d:01:f1:92', #iPad
	'7c:d5:66:cc:ab:fe', #Kindle10
	'8c:86:1e:ce:d3:f4', #RioPhone11
	'ac:1f:74:c2:47:66' #KazPhoneX
]

def driver_init():
	options = Options()
	options.add_argument('-headless')
	driver = webdriver.Firefox(options=options)
	driver.get(url)
	driver.set_window_size(2048, 2048)
	return driver

def go_to_advanced():
	elem = wait.until(expected_conditions.element_to_be_clickable((By.ID,"form_PASSWORD"))) #パスワード
	elem.send_keys('TP2aLYpP')
	elem = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"button_login"))) #ログイン
	elem.click()
	try:
		elem = driver.find_element_by_class_name("errortxt")
		elem = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"button_login"))) #ログイン
		elem.click()
	except:
		pass
	elem = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"panel_advanced"))) #詳細設定
	elem.click()
	elem = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"WIRELESS"))) #無線設定
	elem.click()
	elem = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"FILTER"))) #MACアクセス制限
	elem.click()
	iframe = driver.find_element_by_id("content_main") #内部のiframe
	driver.switch_to.frame(iframe)
	elem = wait.until(expected_conditions.element_to_be_clickable((By.ID,"label_t19_mac"))) #登録リストの編集
	elem.click()

def enable(list_to_be_added):
	sleep(3) #FIXME
	elem = wait.until(expected_conditions.visibility_of_element_located((By.ID,"id_wificontrollist"))) #登録するMACアドレス
	for v in list_to_be_added:
		elem.send_keys(v)
		elem.send_keys(Keys.ENTER)
	elem = wait.until(expected_conditions.element_to_be_clickable((By.ID,"label_t7_mac_reg"))) #新規追加
	elem.click()
	wait_for_progress()
	elem = wait.until(expected_conditions.element_to_be_clickable((By.ID,"label_t2_mac_reg"))) #編集を終了して前の画面へ戻る
	elem.click()

def disable(list_to_be_deleted):
	trs = driver.find_element_by_xpath("/html/body/table[@id='id_reg_list']").find_elements(By.TAG_NAME, "tr")
	while(len(trs) == 1):
		sleep(0.2)
		trs = driver.find_element_by_xpath("/html/body/table[@id='id_reg_list']").find_elements(By.TAG_NAME, "tr")
	deleted = 0
	for i in range(2, len(trs) + 1):
		elem = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "/html/body/table[@id='id_reg_list']/tbody/tr[" + str(i - deleted) + "]/td[1]")))
		if elem.text.lower() in list_to_be_deleted:
			elem = wait.until(expected_conditions.element_to_be_clickable((By.XPATH, "/html/body/table[@id='id_reg_list']/tbody/tr[" + str(i - deleted) + "]/td[2]/input[2]")))
			elem.click()
			wait_for_progress()
			deleted += 1

def logout():
	driver.switch_to.default_content()
	elem = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME,"statusIcon.status_logout"))) #ログアウト
	elem.click()
	driver.close()

def wait_for_progress():
	driver.switch_to.default_content()
	wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME,"progress")))
	wait.until(expected_conditions.invisibility_of_element_located((By.CLASS_NAME,"progress")))
	iframe = driver.find_element_by_id("content_main")
	driver.switch_to.frame(iframe)

driver = driver_init()
wait = WebDriverWait(driver, 10)

go_to_advanced()

if sys.argv[1] == "enableall":
	enable(limited + unlimited)

elif sys.argv[1] == "enable":
	enable(limited)

elif sys.argv[1] == "disable":
	disable(limited)

elif sys.argv[1] == "disableall":
	disable(limited + unlimited)

logout()
