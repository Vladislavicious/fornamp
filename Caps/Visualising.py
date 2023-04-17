"""функции для отображения информации"""
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List
from datetime import datetime

from Caps.listFuncs import *
from Caps.sorting import *


def SaveBarplot(data: pd.Series, startDate: datetime, endDate: datetime, title: str = ""):
    """Сохраняет график в рабочей директории"""
    series = data[startDate:endDate]

    label_rotation = 45
    if (series.size > 75):
        label_rotation = 90

    fig, ax = plt.subplots(figsize=(16, 8))    
    fig = sns.barplot(x=series.index, y=series.values, ax=ax)

    x_labels = series.index.strftime('%d-%m-%Y')

    ax.set_title(title)
    ax.set_ylabel("Проделанная работа, раб. коэф")
    ax.set_xticklabels(labels=x_labels, rotation=label_rotation, ha='right')

    save_fig = fig.get_figure()
    save_fig.savefig(title+".png")


def SaveLinechartComparison(startDate: datetime, endDate: datetime, series_list: List[pd.Series], title: str = ""):
    series = list()
    for ser in series_list:
        series.append(ser[startDate: endDate])
    
    x_labels = pd.date_range(startDate, endDate, freq="D")

    df = pd.DataFrame(index=x_labels)
    for ser in series:
        df[ser.name] = ser

    fig, ax = plt.subplots(figsize=(16, 8))    
    fig = sns.lineplot(data=df, ax=ax)

    ax.set_title(title)
    ax.set_ylabel("Проделанная работа, раб. коэф")

    save_fig = fig.get_figure()
    save_fig.savefig(title+".png")
