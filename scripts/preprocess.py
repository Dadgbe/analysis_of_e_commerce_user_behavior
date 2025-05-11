# -*- coding: cp1251 -*-
import pandas as pd
import os 
import glob


def load_data(nrows=None):
    """
    ��������� ��� CSV-����� �� data_raw/ � ���������� � ���� DataFrame.
    """
    pattern = os.path.join("data_raw", "*.csv")
    files = glob.glob(pattern)
    if not files:
        raise FileNotFoundError(f"�� ������� CSV � data_raw/: {pattern}")

    dfs = []
    for f in files:
        print(f"�������� ������ �� {f} ...")
        dfs.append(pd.read_csv(f, nrows=nrows))
    df = pd.concat(dfs, ignore_index=True)
    return df


def clean_data(df):
    print("������� ������")
    #������� ������ � ������������� category_code
    df = df.dropna(subset=['category_code'])
    #������� ����� ���������
    df = df.drop_duplicates()   
    #������� ������ � ������������� ���������� (��������, ������� ����)
    df = df[df['price'] > 0]   
    return df 



def add_features(df):
    print("���������� ����� ���������")   
    #����������� event_time � datetime
    df['event_time'] = pd.to_datetime(df['event_time'], utc=True) 
    #��������� ����, ��� � �.�.
    df['event_date'] = df['event_time'].dt.date
    df['event_hour'] = df['event_time'].dt.hour   
    return df


def save_processed_data(df, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"������������ ������ ��������� � {out_path}")
    


def main():
    df = load_data()
    
    df = clean_data(df)
    df = add_features(df)
    save_processed_data(df, 'data_processed/events_clean.csv')


if __name__ == "__main__":
    main()