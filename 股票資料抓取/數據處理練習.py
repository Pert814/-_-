# -*- coding: utf-8 -*-
import numpy as np
import datetime
from 爬蟲練習 import fetch_data_VWAP
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
def main(): 
    current_year = datetime.datetime.now().year
    stock_NO = input("請輸入股票代碼:")
    data = fetch_data_VWAP(current_year,stock_NO)
    average_price = data
    while True:
        data = fetch_data_VWAP(current_year-1,stock_NO)
        if data is not None:
            current_year -= 1
            if len(data) == 12:
                average_price = np.insert(average_price,0,data)
            else:
                data = None
                print(f"Data from:{current_year}")
        else:
            break
    # 轉換為浮點數
    average_price = np.array([float(i) for i in average_price])
    x_data = np.arange(len(average_price))
    # 定義指數模型
    def exp_model(x, b):
        a = min(average_price) 
        return a * np.exp(b * x)
    print(average_price)
    print(x_data)
    #使用 curve_fit 進行擬合
    popt, pcov = curve_fit(exp_model, x_data, average_price)
    b = popt[0]
    print(f"Fitted parameters: b = {b}")
    y_fit = exp_model(x_data, *popt)

    #繪製原始數據和擬合曲線
    plt.scatter(x_data, average_price, label="average_price", color='blue', alpha=0.5)
    plt.plot(x_data, y_fit, label="Exponential Fit", color='red')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Exponential Fit')
    # 儲存圖表為圖片檔案
    plot_file = f"{stock_NO}指數擬合曲線.png"
    plt.savefig(plot_file)
    plt.show()  
    plt.close()

if __name__ == "__main__":
    main()