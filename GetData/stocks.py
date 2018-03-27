import psycopg2
import quandl
from datetime import date
import csv

conn = psycopg2.connect(host="localhost",database="invest", user="malaika", password="")
conn.autocommit = True
cur=conn.cursor()

print(conn.closed)
quandl.ApiConfig.api_key = 'dsKEcKZQ99a3barLQysK'

insert_command="""INSERT INTO nse_stocks
                  values ({},{},{},{},{},{},{},{},{},{})"""
update_command="""UPDATE nse_stocks
                  set timestamp={}, open={}, high={}, low={}, last={}, close={}, total_trade_qty={}, turnover={}
                  where company_id={}"""
update_historic_command="""INSERT INTO timeseries_stocks
                            values({},{},{})"""
select_historic_command="""SELECT timestamp, close,company_id
                            from nse_stocks
                            where company_id={}"""

with open('/Users/malaika/Desktop/auxDBMS/stocks_meta.csv','r') as fp:
    with open ('/Users/malaika/Desktop/auxDBMS/stocks.csv','w') as f:
        writer=csv.writer(f)
        records=csv.reader(fp)
        count=0
        date=str(date.today())
        for row in records:
            if(row[2]!='Unavailable'):
                print(d)
                count+=1
                print(count)
                code=row[0]
                code=code[code.find('/')+1::]
                try:
                    result=quandl.get(row[0],start_date=date,end_date=date).values[0]
                    command=insert_command.format("'"+row[1]+"'","'"+code+"'","'"+date+"'",result[0],result[1],result[2],result[3],result[4],result[5],result[6])
                    #command=update_command.format("'"+date+"'",result[0],result[1],result[2],result[3],result[4],result[5],result[6],"'"+code+"'") #uncomment this after the first time the dataset gets populated
                    c=select_historic_command.format("'"+code+"'")
                    cur.execute(c)
                    d=cur.fetchone()
                    print(d)
                    update_historic=update_historic_command.format("'"+d[2]+"'",d[1],"'"+str(d[0])+"'")
                    cur.execute(update_historic)
                    #writer.writerow([row[1],code,date,result[0],result[1],result[2],result[3],result[4],result[5],result[6]])
                    cur.execute(command)
                    #print(result)
                except Exception as e:
                    print(e)