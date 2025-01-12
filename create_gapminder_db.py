import pandas as pd
import sqlite3
import sys

#檢查環境名稱
print(sys.executable)


class CreateGapminderDB():
    def __init__(self):
      #CSV檔案名稱
      self.file_names = [
          "ddf--datapoints--gdp_pcap--by--country--time",
          "ddf--datapoints--lex--by--country--time",
          "ddf--datapoints--pop--by--country--time",
          "ddf--entities--geo--country"
          ]

      #SQL資料庫Table名稱
      self.table_names = [
          "gdp_per_capita",
          "life_expectancy",
          "population",
          "geography"
          ]

    def import_as_dataframe(self):
      #將CSV轉換成字典
      df_dict = dict()

      for file_name, table_name in zip(self.file_names, self.table_names):
          file_path = f"data/{file_name}.csv" #相對路徑
          df = pd.read_csv(file_path)
          df_dict[table_name] = df

      return df_dict

    def create_database(self):
      #將字典轉換成DB(key=table_name; value=df)
      connection = sqlite3.connect("data/gapminder.db")
      df_dict = self.import_as_dataframe()  #先執行func回傳df
      for key, value in df_dict.items():
          value.to_sql(name=key, con=connection, index=False, if_exists="replace")

      #若存在先刪除
      drop_view_sql = """
      DROP VIEW IF EXISTS plotting;
      """

      #建立檢視表VIEW
      create_view_sql = """
      CREATE VIEW plotting AS
      SELECT gdp_per_capita.time AS dt_year,
            gdp_per_capita.gdp_pcap AS gdp_per_capita,
            geography.name AS country_name,
            geography.world_4region AS continent,
            life_expectancy.lex AS life_expectancy,
            population.pop AS population
        FROM gdp_per_capita
        JOIN geography 
          ON gdp_per_capita.country = geography.country
        JOIN life_expectancy 
          ON gdp_per_capita.country = life_expectancy.country AND
            gdp_per_capita.time = life_expectancy.time
        JOIN population
          ON gdp_per_capita.country = population.country AND
            gdp_per_capita.time = population.time
      WHERE gdp_per_capita.time < 2024;
      """

      cur = connection.cursor()
      cur.execute(drop_view_sql)      #執行drop view語法
      cur.execute(create_view_sql)    #執行create view語法
      connection.close()

#檢查class是否正常運作
create_gapminder_db = CreateGapminderDB()
create_gapminder_db.create_database()