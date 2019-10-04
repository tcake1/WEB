import pandas as pd
from models import db,Minwon
import sqlalchemy as sql
from minwon_search import set_query_topic,district_stats

sql_engine = sql.create_engine('sqlite:///final_data.db')

data = pd.read_sql_table('minwon_table',sql_engine)

data.date = pd.to_datetime(data.date)

a = data[data.date > '2018-08-01']
a.date = a.date.astype(str)

print(district_stats(a,set_query_topic('송파구 가로등 보수작업')))
