import psycopg2
from bs4 import BeautifulSoup
from requests import get
import datetime
import csv

conn = psycopg2.connect(host="localhost",database="money", user="malaika", password="")
conn.autocommit = True
cur=conn.cursor()

alter_command="""UPDATE Mutual_Funds
                set price={},three_mo_ret={},ytd_ret={}
                where fund_code={}"""

offset=0
links=[]
with open("mutualfunds.csv",'w') as f:

    writer=csv.writer(f)
    while(offset<1500):
        url='https://finance.yahoo.com/mutualfunds?offset={}&count=100'.format(offset)
        print(url)
        data=get(url).text
        soup=BeautifulSoup(data,'lxml')

        table=soup.find('table')
        rows=table.find_all('tr')
        for row in rows:
            l=[]
            cell=row.find_all("td")
            for s in cell:
                link=''
                try:
                    children=s.findChildren()
                    if(children):
                        for child in children:
                            text=child.text
                            #uncomment this part the first time you run it
                            '''if(child.name=='a'):
                                link=child['href']
                                link="https://finance.yahoo.com"+link
                                link=link.replace('?','/profile'+'?')
                                links.append(link)
                                d=get(link).text
                                s=BeautifulSoup(d,'lxml')
                                y=s.find('span',{'data-reactid':"40"}).text
                                if(y=='Fund Family'):
                                    y="N/A"'''
                                
                                    
                            if((not(text.startswith('+') and not(text.startswith('-')))) and not(text.startswith('0.00'))):
                                try:
                                    l.append(text)
                                    #l.append(float(text))
                                except Exception as e:
                                    print(e)
                    else:
                        try:
                            l.append(float(s.text))
                        except:
                            l.append(s.text)
                            
                except Exception as e:
                    print(e)
            #print(l)
            if(l):
                #alter_command=alter_command.format(l[2],"'"+l[5]+"'","'"+l[6]+"'","'"+l[0]+"'")
                
                #cur.execute(alter_command)
                
                #uncomment this the first time you run this
                print(l)
                d=str(datetime.date.today())
                try:
                    #insert_command=insert_command="INSERT INTO Mutual_Funds values ({},{},{},{},{},{})".format("'"+l[0]+"'","'"+l[1]+"'","'"+d+"'",l[2],"'"+l[5]+"'","'"+l[6]+"'")
                    insert_command=insert_command="INSERT INTO Mutual_Funds values ({},{},{},{},{},{})".format("'"+l[0]+"'","'"+l[1]+"'","'"+d+"'",l[2],"'"+l[5]+"'","'"+l[6]+"'")
                    print(insert_command)
                    cur.execute(insert_command)
                    writer.writerow([l[0],l[1],d,l[2],l[5],l[6]])
                except Exception as e:
                    print(e)

        offset+=100
    with open('/Users/malaika/Desktop/mutual_funds_meta.csv','r') as fp:
        reader=csv.reader(fp)
        for row in reader:
            c="""update mutual_funds set category={} where fund_code={}""".format("'"+row[2]+"'","'"+row[1]+"'")
            cur.execute(c)
    '''for url in links:
    	d=get(url).text
    	s=BeautifulSoup(d,'lxml')
    	y=s.find('span',{'data-reactid':"40"}).text
    	if(y=='Fund Family'):
    	    y="N/A"
    	x=s.find("h1").text
    	x=x[:x.find(" -")]
    		# print(x,y)
    	c="""update mutual_funds set category={} where fund_code={}""".format("'"+y+"'","'"+x+"'")
    	cur.execute(c)'''