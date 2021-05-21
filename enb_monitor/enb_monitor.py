import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
import datetime

def init():
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus'] = False

def enb_num_view(start_time,end_time = 0,mme = 'MME0C'):
    init()
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    if 0 == end_time:
        end_time = pd.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        end_time = pd.to_datetime(end_time,format='%Y%m%d')
        end_time = datetime.datetime.strftime(end_time,'%Y-%m-%d %H:%M:%S')
    start_time = pd.to_datetime(start_time,format='%Y%m%d')
    start_time = datetime.datetime.strftime(start_time,'%Y-%m-%d %H:%M:%S')
    sql = 'select entity_name,enb_num,date_time from mme_data where entity_name=\''+mme+'\''+\
          ' and date_time >= \''+start_time+'\' and date_time <= \''+ end_time+'\' and date_time like \'20__-__-__ 10:55:__\''
    #print(sql)
    df = pd.read_sql(sql, engine)
    quiretime = df['date_time'].apply(lambda x:x.strftime('%m-%d'))
    recs = plt.bar(quiretime, df['enb_num'])

    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x() + rec.get_width() / 2, h, int(h), ha='center', va='bottom',fontsize=7)
    plt.xticks(rotation=-90)
    plt.title("山区六地市eNodeB数量")
    plt.show()


if __name__ == '__main__':
    enb_num_view('20210501',mme='MME0C')