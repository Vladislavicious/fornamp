"""функции для отображения информации"""
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
import seaborn as sns

from Caps.listFuncs import *
from Caps.sorting import *
import BaH

def SaveBarplot(data : pd.Series, startDate : datetime.datetime, endDate : datetime.datetime, title: str = ""):
    """Сохраняет график в рабочей директории"""
    series = data[startDate:endDate]

    label_rotation = 45
    if(series.size > 75):
        label_rotation = 90

    fig, ax = plt.subplots(figsize = (16,8))    
    fig = sns.barplot(x = series.index, y = series.values, ax=ax)

    x_labels = series.index.strftime('%d-%m-%Y')

    ax.set_title(title)
    ax.set_ylabel("Проделанная работа, раб. коэф")
    ax.set_xticklabels(labels=x_labels, rotation=label_rotation, ha='right')

    save_fig = fig.get_figure()
    save_fig.savefig(title+".png")


