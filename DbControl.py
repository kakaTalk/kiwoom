import sqlite3
import pandas as pd
from pandas import DataFrame

class DbCon:
    def __init__(self, name):
        self.con = sqlite3.connect(name)
        self.cursor = self.con.cursor()

    def save_dataframe_to_db(self, df, tableName):
        df.to_sql(name=tableName, con=self.con , if_exists='append')
        #self.con.commit()       #수행한 내용 반영

    def read_db_to_dataframe(self, query):
        return pd.read_sql(query, con=self.con, index_col=None)

    def _select_FROME_table(self, tablName):
        return "SELECT * FROM '" + tablName+"'"

    def _where_by(self, colume, num):
        return "WHERE " + colume + str(num) + " "

    def _oreder_by(self, colume):
        return "ORDER BY " + colume

    #query = "SELECT * FROM 024060 OREDER BY date"