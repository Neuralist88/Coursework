import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from model import df_salary, df_inflation, man, edu, med, years, years_2001, inflation, man_infl, edu_infl, med_infl 


# Добвим заголовок приложения
st.title('Старт в DS. Итоговое задание')

on = st.toggle("Показать исходные данные")

if on:    
    st.write("Исходные данные об уровне заработной платы")
    st.write(df_salary)

    st.write('Исходные данные об уровне инфляции')
    st.write(df_inflation) 

    fig, ax = plt.subplots()
    ax.plot(years, man, label='производство электроники')
    ax.plot(years, edu, label='образование')
    ax.plot(years, med, label='медицина')
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10000))
    ax.set_ylabel('Средняя заработная плата, руб.')
    ax.legend()
    ax.set_title('График изменения заработной платы в период 2000-2023 гг.')
    ax.grid()
    st.pyplot(fig)
    
    fig, ax = plt.subplots()
    ax.plot(years, inflation)
    ax.xaxis.set_ticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.set_ylabel('Среднегодовой уровень инфляции, %, руб.')
    ax.grid()
    ax.set_title('График изменения уровня инфляции за период 2000-2023 гг.')
    st.pyplot(fig)

# Добавим кнопку, при нажатии на которую отображаются какие-то данные
def click_button():
    st.session_state.button = not st.session_state.button

if 'button' not in st.session_state:
    st.session_state.button = False

# Опишем, что должно происходить при нажатии на кнопку
st.button('Поcмотреть реальный рост зарплат', on_click=click_button)
if st.session_state.button:
    branch = st.radio(
    "Выберите интересующую отрасль",
    ["Производство электроники", "Образование", "Медицина"],
    index=None)
    fig, ax = plt.subplots()
    if branch=="Производство электроники":
        ax.plot(years_2001, man_infl, label='производство электроники')
    elif branch=="Образование":
        ax.plot(years_2001, edu_infl, label='образование')
    elif branch=="Медицина":
        ax.plot(years_2001, med_infl, label='медицина')
    ax.xaxis.set_ticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.set_xlim(2001, 2023)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.set_ylabel('Прирост средней заработной платы относительно предыдущего года, %.', fontsize=10, wrap=True, labelpad=5)    
    ax.grid()
    ax.set_title('График реального изменения зарплат с учетом инфляции')
    st.pyplot(fig)
