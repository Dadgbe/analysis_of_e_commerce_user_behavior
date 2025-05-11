# scripts/compute_metrics.py

import os
import pandas as pd

def load_clean_data(filepath, nrows=None):
    """Загрузить предварительно очищенные и обогащённые данные."""
    print(f"Загрузка очищенных данных из {filepath}...")
    return pd.read_csv(filepath, parse_dates=['event_time'], nrows=nrows)

def compute_dau(df):
    """Daily Active Users (DAU)."""
    return (
        df.groupby(df['event_time'].dt.date)['user_id']
          .nunique()
          .rename('DAU')
    )

def compute_wau(df):
    """Weekly Active Users (WAU)."""
    week = df['event_time'].dt.to_period('W').apply(lambda r: r.start_time.date())
    return (
        df.assign(week=week)
          .groupby('week')['user_id']
          .nunique()
          .rename('WAU')
    )

def compute_mau(df):
    """Monthly Active Users (MAU)."""
    month = df['event_time'].dt.to_period('M').apply(lambda r: r.start_time.date())
    return (
        df.assign(month=month)
          .groupby('month')['user_id']
          .nunique()
          .rename('MAU')
    )

def compute_conversion_rate(df):
    """Conversion rate = unique purchase sessions / unique view sessions."""
    views = df[df['event_type']=='view']['user_session'].nunique()
    purchases = df[df['event_type']=='purchase']['user_session'].nunique()
    rate = purchases / views if views else 0
    return pd.Series({'ConversionRate': rate})

def compute_aov_arpu(df):
    """Average Order Value (AOV) и ARPU."""
    purchases = df[df['event_type']=='purchase']
    total_rev = purchases['price'].sum()
    num_orders = purchases.shape[0]
    users = df['user_id'].nunique()
    aov = total_rev / num_orders if num_orders else 0
    arpu = total_rev / users if users else 0
    return pd.Series({'AOV': aov, 'ARPU': arpu})

def compute_retention(df, days=1):
    """
    Retention D{days}: доля пользователей, вернувшихся через days дней
    после первого события.
    """
    df = df.copy()
    df['event_date'] = df['event_time'].dt.date
    first = df.groupby('user_id')['event_date'].min().rename('first_date').reset_index()
    merged = df.merge(first, on='user_id')
    merged['target'] = merged['first_date'] + pd.Timedelta(days=days)
    retained = merged[merged['event_date']==merged['target']]['user_id'].nunique()
    total = first['user_id'].nunique()
    rate = retained / total if total else 0
    return pd.Series({f'Retention_D{days}': rate})

def compute_top_products(df, n=10):
    """Топ n продуктов по выручке с category_code и brand."""
    purchases = df[df['event_type']=='purchase']
    metrics = purchases.groupby('product_id')['price']\
                       .agg(revenue='sum', orders='count')
    info = df[['product_id','category_code','brand']].drop_duplicates('product_id').set_index('product_id')
    top = (metrics.join(info, how='left')
                  .sort_values('revenue', ascending=False)
                  .head(n)
                  .reset_index())
    return top

def assemble_metrics(df):
    """Собрать все временные ряды и статические метрики."""
    # временные ряды
    dau = compute_dau(df)
    wau = compute_wau(df)
    mau = compute_mau(df)
    ts = pd.concat([dau, wau, mau], axis=1).reset_index().rename(columns={'index':'period'})

    # статические
    conv = compute_conversion_rate(df)
    aos = compute_aov_arpu(df)
    r1  = compute_retention(df, days=1)
    r7  = compute_retention(df, days=7)
    static = pd.concat([conv, aos, r1, r7])

    # топ-продукты
    top = compute_top_products(df, n=10)

    return ts, static, top

def save_metrics(ts, static, top, dir_path='data_processed'):
    os.makedirs(dir_path, exist_ok=True)

    # Временные ряды
    ts_path = os.path.join(dir_path, 'user_metrics_timeseries.csv')
    ts.to_csv(ts_path, index=False)
    print(f"Временные ряды сохранены в {ts_path}")

    # Статические метрики
    static_path = os.path.join(dir_path, 'user_metrics_static.csv')
    static.to_frame(name='value').to_csv(static_path, index=True)
    print(f"Статические метрики сохранены в {static_path}")

    # Топ-продукты
    top_path = os.path.join(dir_path, 'top_products.csv')
    top.to_csv(top_path, index=False)
    print(f"Топ-{top.shape[0]} продуктов сохранён в {top_path}")

def main():
    df = load_clean_data('data_processed/events_clean.csv')
    print("Расчёт метрик...")
    ts, static, top = assemble_metrics(df)
    save_metrics(ts, static, top)

if __name__ == '__main__':
    main()
