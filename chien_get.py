#coding:utf-8

from selenium import webdriver

PHANTOMJS_PATH = "C:\\Program Files (x86)\\phantomjs-2.0.0-windows\\bin\\phantomjs.exe"
driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)

def get_keio_line(url):
	driver.get(url)

	table = driver.find_element_by_tag_name("table") #遅延証明書一覧テーブル
	tr_list = table.find_elements_by_tag_name("tr")[5:] #データ部分

	i = 0
	file_name = ""
	for tr in tr_list:
		if i == 0: #日付&17:00~24:00
			ymd = tr.find_elements_by_tag_name("th")[0].text.split("\n") #日付取得
			file_name = ymd[0] + ymd[1] + "_京王線" + ".png"
			i += 1
		elif i == 1: #10:00~17:00
			i += 1
		elif i == 2: #初電〜10:00
			td = tr.find_elements_by_tag_name("td")[0] #京王線上り
			try:
				a = td.find_element_by_tag_name("a") #リンクの有無
				a.click()
				driver.switch_to.window(driver.window_handles[-1])
				driver.save_screenshot(file_name)
				print "save screenshot... " + file_name
				driver.close()
				driver.switch_to.window(driver.window_handles[0])
			except:
				pass
			i = 0

def get_shinjuku_line(url):
	driver.get(url)

	table = driver.find_elements_by_tag_name("table")[2] #遅延証明書一覧テーブル
	td_list = table.find_elements_by_tag_name("td") #データ部分

	for td in td_list:
		if td.text.find(u"始発～10:00") > -1:
			file_name = td.text.split()[0] + u"_新宿線" + ".png"
			try:
				a = td.find_element_by_tag_name("a") #リンクの有無
				a.click()
				driver.switch_to.window(driver.window_handles[-1])
				driver.save_screenshot(file_name)
				print "save screenshot... " + file_name
				driver.close()
				driver.switch_to.window(driver.window_handles[0])
			except:
				pass

if __name__ == "__main__":
	if driver != None:
		try:
			get_keio_line("http://www.keio.co.jp/train/delay")
			get_shinjuku_line("http://www.kotsu.metro.tokyo.jp/subway/schedule/delay.html")
		except:
			pass
		finally:
			driver.quit()

	print "...get chien-cert finished"
