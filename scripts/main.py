# -*- coding: cp1251 -*-
import os
import sys
import pandas as pd

csv_path = "data_processed/events_clean.csv"

if os.path.exists(csv_path):
    # Загружаем первые 10 строк
    df_sample = pd.read_csv(csv_path, nrows=10000000)
    print("\nИнформация о загруженных данных:")
    print(df_sample.info())
    
    print("\nПервые 10 строк файла:")
    print(df_sample.head(10000000))  # выводим таблицу как есть
else:
    print("Ошибка: файл не найден по пути: ", os.path.abspath(csv_path))
    sys.exit(7)
