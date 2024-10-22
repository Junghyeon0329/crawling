from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# https://googlechromelabs.github.io/chrome-for-testing/
service = Service('C:\\Users\\Choi\\Desktop\\chromedriver-win64\\chromedriver.exe') 
driver = webdriver.Chrome(service=service)

date_range = pd.date_range(start='2023-09-01', end='2024-09-01', freq='MS')  # 월 시작

for date in date_range:
	date_index = date.strftime('%Y-%m-00')  # 'YYYY-MM-00' 형식으로 변환
	print("date_index:", date_index)
	url = f'https://auto.danawa.com/auto/?Work=record&Tab=Model&Month={date_index}&MonthTo='
	driver.get(url)

	# 페이지가 로드될 때까지 잠시 대기
	time.sleep(3)

	# XPath를 사용하여 데이터 추출

	store_data = pd.DataFrame([])
	i = 0
	while True:
		i+=1
		rows = driver.find_elements(By.XPATH, f'//*[@id="autodanawa_gridC"]/div[3]/article/main/div/table/tbody/tr[{i}]')
		if not rows:
			print(f"No more data at index {i}. Adding empty record.")
			
			break  # 데이터가 없으므로 루프 종료
	
		for row in rows:
			try:
				data_list = row.text.splitlines()
				percentage_change, previous_value = data_list[3].split()
		
				# DataFrame으로 변환
				df = pd.DataFrame({
					'Index': [data_list[0]],
					'월(month)' : date_index,
					'모델': [data_list[1]],
					'판매량': [data_list[2]],
					'점유율': [percentage_change], 
					'전월대비': [previous_value],  
					'전월대비변화량': [data_list[4]],
					'전년대비': [data_list[5]],
					'전년대비변화량': [data_list[6]],
				})
				store_data = pd.concat([store_data, df], ignore_index=True)
			except Exception as e: 
				pass
	store_data.to_csv(f"{date_index}.csv", encoding='cp949')

