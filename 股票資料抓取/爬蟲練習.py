# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import datetime
import time
import random
# 定義request函式
def fetch_data_VWAP(year, stock_no):
    # 使用 f-string 動態生成 URL
    url = f'https://www.twse.com.tw/zh/trading/historical/fmsrfk.html'
    req = f'https://www.twse.com.tw/rwd/zh/afterTrading/FMSRFK?date={year}0101&stockNo={stock_no}&response=json'

    # 發送請求，延遲以防止封鎖
    response = requests.get(url)
    result = requests.get(req)
    time.sleep(random.uniform(1, 3))
    # 確保請求成功，處理資料
    if result.status_code == 200:
        try:
            data_json = result.json()  # 檢查 JSON 是否包含 'fields' 鍵
            if 'fields' not in data_json:
                print(f"No data found for {stock_no} in {year}")
                return None
            field = data_json['fields']
            target_index = field.index('加權(A/B)平均價')
            data = [row[target_index] for row in data_json['data']]
            return data
        except ValueError as e:
            print(f"Error parsing JSON for {stock_no} in {year}: {e}")
            return None
    else:
        print(f"Error fetching data for {stock_no} in {year}")
        return None
#爬出資料
def main(): 
    current_year = datetime.datetime.now().year
    stock_NO = input("請輸入股票代碼:")
    data = fetch_data_VWAP(current_year,stock_NO)
    average_price = np.pad(data,(0,12-len(data)),constant_values = 0)
    while True:
        data = fetch_data_VWAP(current_year-1,stock_NO)
        if data is not None:
            current_year -= 1
            if len(data) == 12:
                average_price = np.vstack([average_price, data]) if average_price.size else np.array([data])
            else:
                data = None
                print(f"Data from:{current_year}")
        else:
            break
    # 將資料轉換成 DataFrame（Excel 格式）
    current_year = datetime.datetime.now().year
    n_years = average_price.shape[0]
    np_year = np.arange(current_year, current_year - n_years, -1)
    np_month = np.arange(1,13)
    df = pd.DataFrame(average_price, columns=[f"{i}月" for i in np_month],index = [f"{i}年" for i in np_year])
    # 將資料寫入 Excel 檔案
    df.to_excel(f"{stock_NO}月成交資訊.xlsx", index=True, engine='openpyxl') 
if __name__ == "__main__":
    main()



