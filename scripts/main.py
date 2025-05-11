# -*- coding: cp1251 -*-
import os
import sys
import pandas as pd

csv_path = "data_processed/events_clean.csv"

if os.path.exists(csv_path):
    # ��������� ������ 10 �����
    df_sample = pd.read_csv(csv_path, nrows=10000000)
    print("\n���������� � ����������� ������:")
    print(df_sample.info())
    
    print("\n������ 10 ����� �����:")
    print(df_sample.head(10000000))  # ������� ������� ��� ����
else:
    print("������: ���� �� ������ �� ����: ", os.path.abspath(csv_path))
    sys.exit(7)
