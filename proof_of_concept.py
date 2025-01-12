import sqlite3
import pandas as pd
import matplotlib.pyplot as plt             #要先在terminal輸入conda install matplotlib
import matplotlib.animation as animation    #動畫模組
import numpy as np

#從DB載入資料成為DF
connection = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql("""SELECT * FROM plotting;""",con=connection)  
connection.close()

#建立畫布與軸物件
fig, ax = plt.subplots()

#動畫生成函數
def update_plot(year_to_plot: int): #修改成想繪製的年份
    ax.clear()  #清除前一張畫布內容
    subset_df = plotting_df[plotting_df['dt_year'] == year_to_plot]

    #以下df取出values變為ndarray
    lex = subset_df["life_expectancy"].values
    gdp_pcap = subset_df["gdp_per_capita"].values
    cont = subset_df["continent"].values
    pop = subset_df["population"].values

    #print(subset_df["continent"].unique())  #不重複的洲 ['asia' 'africa' 'europe' 'americas']
    color_map = {
        "asia": "r",    # r for red
        "africa":"g",   # g for green
        "europe":"b",   # b for blue
        "americas":"c"  # c for cyan
    }

    scaled_pop = np.interp(pop, (pop.min(), pop.max()), (10, 1000)) #將人口數標準化限定最小與最大值範圍
    color = [color_map[i] for i in cont] #將洲別轉換成顏色代碼

    ax.scatter(x=gdp_pcap, y=lex, s=scaled_pop, c=color, alpha=0.5)
    ax.set_title(f"The world in {year_to_plot}")
    ax.set_xlabel("GDP per capita(in USD)")
    ax.set_ylabel("Life Expectancy(in year)")
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 100000)

    #plt.show()

ani = animation.FuncAnimation(fig=fig, func=update_plot, frames=range(1800, 2024), interval=10)
ani.save("animation.gif", fps=10)