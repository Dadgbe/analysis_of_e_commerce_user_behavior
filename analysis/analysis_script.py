import os
import pandas as pd
import matplotlib.pyplot as plt

def load_metrics():
    ts_path     = 'data_processed/user_metrics_timeseries.csv'
    static_path = 'data_processed/user_metrics_static.csv'
    top_path    = 'data_processed/top_products.csv'

    if not os.path.exists(ts_path):
        raise FileNotFoundError(f"Не найден файл временных рядов: {ts_path}")
    ts = pd.read_csv(ts_path, parse_dates=['period'])

    if not os.path.exists(static_path):
        raise FileNotFoundError(f"Не найден файл статических метрик: {static_path}")
    static = pd.read_csv(static_path, index_col=0)['value']

    if not os.path.exists(top_path):
        raise FileNotFoundError(f"Не найден файл топ-продуктов: {top_path}")
    top = pd.read_csv(top_path)

    return ts, static, top

def plot_timeseries_metrics(ts):
    os.makedirs('analysis/figures', exist_ok=True)
    metrics = [col for col in ts.columns if col != 'period']

    for metric in metrics:
        plt.figure(figsize=(8, 4))
        if ts.shape[0] == 1:
            plt.bar(ts['period'].dt.strftime('%Y-%m-%d'), ts[metric])
        else:
            plt.plot(ts['period'], ts[metric], marker='o')
        plt.title(metric)
        plt.xlabel('Date')
        plt.ylabel(metric)
        plt.xticks(rotation=45)
        plt.tight_layout()
        filename = f'analysis/figures/{metric.lower().replace(" ", "_")}.png'
        plt.savefig(filename)
        plt.close()

def plot_static_metrics(static):
    os.makedirs('analysis/figures', exist_ok=True)
    plt.figure(figsize=(6, 4))
    static.plot(kind='bar')
    plt.title('Статические метрики')
    plt.ylabel('Значение')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('analysis/figures/static_metrics.png')
    plt.close()

def plot_top_products(top):
    os.makedirs('analysis/figures', exist_ok=True)
    plt.figure(figsize=(10, 6))
    labels = top.apply(
        lambda r: f"{r['product_id']} ({r['brand']}, {r['category_code']})", axis=1
    )
    plt.barh(labels, top['revenue'])
    plt.gca().invert_yaxis()
    plt.title('Top-10 Products by Revenue')
    plt.xlabel('Revenue')
    plt.tight_layout()
    plt.savefig('analysis/figures/top_products.png')
    plt.close()

def generate_report(static, ts):
    lines = [
        '# Report on E-commerce User Metrics\n',
        '## Static Metrics\n'
    ]
    for metric, val in static.items():
        lines.append(f'- **{metric}**: {val:.4f}')
    lines.append('\n![](figures/static_metrics.png)\n')

    lines.append('## Time Series Metrics\n')
    metrics = [col for col in ts.columns if col != 'period']
    for metric in metrics:
        lines.append(f'### {metric}\n')
        filename = f'figures/{metric.lower().replace(" ", "_")}.png'
        lines.append(f'![]({filename})\n')

    lines.append('## Top-10 Products by Revenue\n')
    lines.append('![](figures/top_products.png)\n')

    report_path = 'analysis/report.md'
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'Report generated at {report_path}')

def main():
    ts, static, top = load_metrics()
    print("Plotting time series metrics...")
    plot_timeseries_metrics(ts)
    print("Plotting static metrics...")
    plot_static_metrics(static)
    print("Plotting top-10 products...")
    plot_top_products(top)
    print("Generating report...")
    generate_report(static, ts)

if __name__ == '__main__':
    main()
