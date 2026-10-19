import sys
import os

def get_app_folder(): #回傳程式實際所在的資料夾，打包成exe後也能正確指到USB上的執行檔位置
    if getattr(sys, 'frozen', False): #PyInstaller打包後sys.frozen為True，__file__會指向暫存解壓資料夾而非USB路徑
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))
