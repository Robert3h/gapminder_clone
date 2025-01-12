import sqlite3
import pandas as pd
import plotly.express as px   #需要事先conda install plotly

#建立連線與轉換成dataframe
connection = sqlite3.connect("data/gapminder.db")
plotting_df = pd.read_sql("""SELECT * FROM plotting;""", con=connection)
connection.close()

#繪圖
fig = px.scatter(data_frame=plotting_df, 
                 x="gdp_per_capita", 
                 y="life_expectancy", 
                 animation_frame="dt_year",
                 animation_group="country_name",
                 color="continent",
                 size="population",
                 hover_name="country_name",
                 size_max=100,
                 range_x=[500, 100000],
                 range_y=[20, 100],
                 log_x=True,
                 title="Gapminder_Clone_1800-2023")

fig.show()                                              #直接顯示在網頁上
fig.write_html("gapminder_clone.html", auto_open=True)  #產生html檔案