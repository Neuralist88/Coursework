import pandas as pd
import numpy as np
import os
import streamlit as st
import matplotlib.pyplot as plt
from psycopg2 import pool
from dotenv import load_dotenv
from db_connect import sql_to_df, connect

# Load .env file
load_dotenv()

# Get the connection string from the environment variable
connection_string = os.getenv('DATABASE_URL')

#creating a query variable to store our query to pass into the function
query_salary = 'SELECT * FROM "raw_data_salary";'
query_inflation= 'SELECT * FROM "raw_data_inflation";'

#creating a list with columns names to pass into the function
column_names_inflation = ['Год', 'Уровень инфляции']
column_names_salary = ['Отрасль'] + [str(i) for i in range(2000, 2024)]

#opening the connection
conn = connect(connection_string)

#loading our dataframe
df_inflation = sql_to_df(conn, query_inflation, column_names_inflation)
df_salary = sql_to_df(conn, query_salary, column_names_salary)

#closing the connection
conn.close()
# Let’s see if we loaded the df successfully

# Немного преобразуем загруженные датафреймы для удобства их последующей обработки
df_salary = df_salary.iloc[:, 1:].astype(float)
inflation = df_inflation['Уровень инфляции'].values[::-1]
years = np.array(range(2000, 2024))
years_2001 = np.array(range(2001, 2024))
man = df_salary.iloc[0][:]
edu = df_salary.iloc[1][:]
med = df_salary.iloc[2][:]

#Рассчитаем относительное изменение зарплат в % относительно предыдущего года 
df_salary_rel = df_salary.copy(deep=True)
for index, row in df_salary.iterrows():
    for i in range(1,len(row)):
        df_salary_rel.iat[index, i] = (df_salary.iat[index, i] - df_salary.iat[index, i-1]) / df_salary.iat[index, i-1] * 100      

#рассчитаем реальный относительный рост заработной платы с учетом инфляции. Для этого вычтем значение инфляции для каждого года из относительного роста заработной платы за соответствующий год  
df_salary_rel_infl = df_salary.copy(deep=True)
for index, row in df_salary_rel.iterrows():
    for i in range(1,len(row)):
        df_salary_rel_infl.iat[index, i] = df_salary_rel.iat[index, i] - inflation[i - 1]      
df_salary_rel_infl.drop(df_salary_rel_infl.columns[[0]], axis=1, inplace=True)

#Вычленим из общего датафреймма данные по каждой отрасли
man_infl = df_salary_rel_infl.iloc[0]
edu_infl = df_salary_rel_infl.iloc[1]
med_infl = df_salary_rel_infl.iloc[2]