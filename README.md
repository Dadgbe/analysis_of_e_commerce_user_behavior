## Расчет основных метрик на бесплатном датасете
## Общая информация

Этот проект анализирует поведение пользователей на e-commerce платформе, визуилзируя основные метрики активности, статистику и топ-продукты по выручке.

## Структура проекта
```bash
analysis_of_e_commerce_user_behavior/
  analysis/
    figures/
    analysis_script.py
    report.md
  data_processed/
  data_raw/
  scripts/
    compute_metrics.py
    main.py
    preprocess.py
  data_set_download.py
  requirements.txt
  run_all.bat
```

## Установка

1. **Склонируйте репозиторий:**
```bash
git clone https://github.com/Dadgbe/analysis_of_e_commerce_user_behavior.git
cd analysis_of_e_commerce_user_behavior
```
2. **Создайте виртуальное окружение и активируйте его:**
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```
3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```
## Автоматический запуск 
Для автоматического запуска анализа данных, запустите файл **run_all.bat** в корневой папке проекта. 
Данный файл запустит цепочку скриптов data_set_download.py > preprocess.py > compute_metrics.py > analysis_script.py
Результатом выполнения анализа будет 5 графиков и автоматически сгенерированный отчетный файл содержащий информацию по метрикам report.md
### **ВНИМАНИЕ**
Т.к. количество данных для анализа превышает 10 гб, выполнение анализа может быть продолжительно долгим, так же зависит от мощности системы, на котором будет запускаться анализ.

## Ручной запуск
## **1. Запуск скрипта data_set_download.py**
После клонирования репозитория, проект не подразумевает в себе хранение датасета, т.к. он достаточно много весит, его необходимо будет самостоятельно загрузить, запустив скрипт **data_set_download.py**, который загрузит 2 файла 2019-Nov.csv
и 2019-Oct.csv. 
### 
**Примечение:** 
Изначально эти два файла загрузятся по пути C:\Users\user\.cache\kagglehub\datasets\mkechinov\ecommerce-behavior-data-from-multi-category-store\versions\8 и будут скопированы в папку проекта data_raw, после успешного копирования файлы по первоначальному пути можно будет по желанию удалить.

## **2. Запуск скрипта preprocess.py**
Данный скрипт будет выполняться продолжительное время, т.к. датасет очень объемный и много весит. Сначала два файла объеденяются в один DataFrame, далее происходит "очистка" и "причесывание" данных. Результатом работы скрипта будет файл **events_clean.csv**, который будет сохранен в папке **data_processed*

## **3. Запуск скрипта compute_metrics.py**
Данный скрипт загружает обработанные и сгруппированные данные **events_clean.csv** и составляет на основе этих данных следующие метрики:
```bash
1. DAU, WAU, MAU
2. Conversion rate
3. Aov arpu
4. Retention
5. Top products
```
Данные этих метрик будут сохранены в файлах **user_metrics_static.csv** (conversion rate, aov, arpu, retention d1, retention d7), **user_metrics_timeseries.csv** (dau, wau, mau)

## **4. Запуск скрипта analysis_script.py**
Данный скрипт собирает данные метрик и строит на основе этих данных 5 аналитических графиков:
```bash
1. График DAU
2. График WAU
3. График MAU
4. График топ 10 товаров
5. График конверсии, аов, арпу, ретеншн 1 и 7 дня
```
