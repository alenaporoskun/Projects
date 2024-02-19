# Пояснювальна записка та висновок до лабораторного практикуму

Результатом лабораторного практикуму для 3 країн (згідно з варіантом з файлу [tasks.csv](tasks.csv))

1. Bermuda
2. France
3. Panama

є наступні матеріали.

## Кодова база

### Python code

- [script_convert](samples/script_convert.py)


### Jupiter Notebooks

- [jnb sample](samples/sample.ipynb)


#### Scripts
Для запуску докера з Jupiter Notebook.
- [bash example_10_start_docker_compose_study_jupyter](example_10_start_docker_compose_study_jupyter.sh)

або
- [bash example_20_start_docker_cli_study_jupyter](example_20_start_docker_cli_study_jupyter.sh)


### Файли

Файли, необхідні для розвертання віртуального середовища та Jupiter Notebook через docker або docker_compose (до них входять скрипти з пункту Scripts):
- 00_setup_venv.sh
- Dockerfile.study_bd_jupyter
- docker-compose.yml
- requirements.txt
- example_10_start_docker_compose_study_jupyter.sh
- example_20_start_docker_cli_study_jupyter.sh

Файл виводу роботи [script_convert.py](samples/script_convert.py):
- [output__script_convert.txt](samples/output__script_convert.txt)

#### Вхідні дані (разархівовані та сконвертовані дані) з архівів [datasets](Python_projects/Data_analysis_project/datasets):

- oil-prices.zip
- population.zip
- ppp.zip

Архіви були розпаковані в папку [data](data), з них були скопійовані файли csv-формату у папку [src](src).

##### files 1.1 - 1.8 from folder 'src/oil-prices':

- CSV: [brent-daily.csv](Python_projects/Data_analysis_project/src/oil-prices/brent-daily.csv)
- JSON: [brent-daily.json](Python_projects/Data_analysis_project/src/oil-prices/brent-daily.json)
- XLSX [brent-daily.xlsx](Python_projects/Data_analysis_project/src/oil-prices/brent-daily_pandas.xlsx)

Крім brent-daily.csv, також були розпаковані та сконвертовані у формати .csv, .json, .xlsx інші файли, такі як: 
- brent-monthly.csv, brent-weekly.csv, brent-year.csv, 
- wti-daily.csv, wti-monthly.csv, wti-weekly.csv, wti-year.csv.

##### file 2 from folder [src/population](Python_projects/Data_analysis_project/src/population):

- CSV: population.csv
- JSON: population.json
- XLSX: population_pandas.xlsx

##### file 3 from folder [src/ppp](Python_projects/Data_analysis_project/src/ppp):

- CSV: ppp-gdp.csv
- JSON: ppp-gdp.json
- XLSX: ppp-gdp_pandas.xlsx

#### Сгенеровані нові дані
  
[samples/tables_and_graphs](Python_projects/Data_analysis_project/samples/tables_and_graphs):  
  
##### table 1 in 3 formats

- data_population_1960_2020.csv
- data_population_1960_2020.json
- data_population_1960_2020.xlsx

##### tables 2 - 8

- statistics_population.csv
- statistics_ppp.csv
- statistics_oil.csv
- correlation_oil_ppp.csv
- df_percentage_ppp.csv
- correlation_population_ppp.csv
- correlation_population_oil.csv

#### Графіки

![line1_population.png]([Python_projects/Data_analysis_project/samples/tables_and_graphs/line1_population.png](https://github.com/alenaporoskun/Projects/blob/main/Python_projects/Data_analysis_project/samples/tables_and_graphs/line1_population.png))

- ![line2_population.png](Python_projects/Data_analysis_project/samples/tables_and_graphs/line2_population.png)
- ![line2_population.jpg](Python_projects/Data_analysis_project/samples/tables_and_graphs/line2_population.jpg)
- [line2_population.pdf](Python_projects/Data_analysis_project/samples/tables_and_graphs/line2_population.pdf)

- ![pie_population.png](Python_projects/Data_analysis_project/samples/tables_and_graphs/pie_population.png)
- ![bar_population.png](Python_projects/Data_analysis_project/samples/tables_and_graphs/bar_population.png)

---

## Інструкція до роботи

1. Запускаємо [script_convert](Python_projects/Data_analysis_project/samples/script_convert.py).

2. Результат script_convert:
    1. Розпакування .zip архівів в папку [data](Python_projects/Data_analysis_project/data).
    2. Копіювання необхідних файлів з даними у папку [src](Python_projects/Data_analysis_project/src).
    3. Конвертування csv-файлів у формати .json та .xlsx.

3. Виконуємо код [jnb sample](Python_projects/Data_analysis_project/samples/sample.ipynb) в Jupiter Notebook.

4. Результат [jnb sample](Python_projects/Data_analysis_project/samples/sample.ipynb)
    1. Створює табличку "Популяції за інтервал часу 1960-2020" за відповідним варіантом 3-х форматах (.csv, .json, .xlsx):
    2. Графічно відображає дані з таблички п.1 у 3-х стилях: лінійний(у 2 варіантах), секторний та гістограмний у 3-х форматах (.png, .jpg, .pdf).
    3. Відображає в табличному вигляді основні стаститичні величини: min, max, mean, квантіли 25%, 75%, 95%. 
    4. Показує по роках по кожній країні для відповідного варіанта зв'язок між іншими datasets (для яких є дані):
        
        I. зв'язок ціни на нафту з ppp:
          * [correlation_oil_ppp.csv](Python_projects/Data_analysis_project/samples/tables_and_graphs/correlation_oil_ppp.csv)
        
        II. відсоток ppp окремої країни до середнього ppp всіх країн за рік:
          * [df_percentage_ppp.csv](Python_projects/Data_analysis_project/samples/tables_and_graphs/df_percentage_ppp.csv)
        
        III. зв'язок популяції та ppp:
          * [correlation_population_ppp.csv](Python_projects/Data_analysis_project/samples/tables_and_graphs/correlation_population_ppp.csv)
        
        IV. зв'язок популяції та цін на нафту:
          * [correlation_population_oil.csv](Python_projects/Data_analysis_project/samples/tables_and_graphs/correlation_population_oil.csv)
       
