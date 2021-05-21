import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime,timedelta


if __name__=='__main__':
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    mpl.rcParams['axes.unicode_minus']=False
    engine = create_engine("mysql+pymysql://monitor:12345678@10.209.83.235:3306/epc_data?charset=utf8", echo=False)
    sdate = pd.datetime.now().strftime('%Y-%m-%d ') + '10:35:0_'
    # sql = 'select DATE_FORMAT(date_time,\'%%m-%%d\') date,round(sum(atta_4g_num)/10000,1) num_4g from mme_data where entity_name like \'MME2_\' and date_time like ' + '\'2020-__-__ 11:35:__\' ' \
    #     'and date_time > \'2020-04-28 00:00:00\' group by date_time'
    sql = 'select DATE_FORMAT(date_time,\'%%m-%%d\') date,ROUND(sum(atta_4g_num)/10000) num_4g from mme_data where entity_name like \'MME2_\' and date_time like ' + '\'202_-__-__ 11:35:__\' ' \
          'and date_time > \'2021-01-01 00:00:00\' group by date_time'

    df = pd.read_sql(sql, engine)
    #rs = pd.datetime.now().strftime('%Y-%m-%d ') + '厦门MME附着用户数' + str(round(df['num_4g'][0] / 10000, 1)) + '万'
    tick_label = list(df['date'])
    y = list(df['num_4g'])
    recs = plt.bar(tick_label,y)

    for rec in recs:
        h = rec.get_height()
        plt.text(rec.get_x()+rec.get_width()/2,h,int(h),ha='center',va='bottom')
    plt.xticks(rotation = -90)




    plt.show()
