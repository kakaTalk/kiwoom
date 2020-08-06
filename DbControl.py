import sqlite3

class DbCon:
    def __init__(self, name):
        self.con = sqlite3.connect(name)
        self.cursor = self.con.cursor()

    def save_dataframe_to_db(self, df, tableName):
        df.to_sql(name=tableName, con=self.con , if_exists='append')
        #self.con.commit()       #수행한 내용 반영