import psycopg2

conn = psycopg2.connect(host="localhost",database="invest", user="malaika", password="")
conn.autocommit = True
cur=conn.cursor()

#print(conn.closed)

command="""
        CREATE TABLE Mutual_Funds(
            fund_code varchar(20),
            fund_name varchar(100),
            price numeric,
            three_mo_ret varchar(10),
            ytd_ret varchar(10),
            category varchar(50) default null
        )
        """
cur.execute(command)

alter_command="""UPDATE Mutual_Funds
                set price={},three_mo_ret={},ytd_ret={}
                where fund_code={}"""

from bs4 import BeautifulSoup
from requests import get

offset=0
links=[]
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
                        if(child.name=='a'):
                            link=child['href']
                            link="https://finance.yahoo.com"+link
                            link=link.replace('?','/profile'+'?')
                            links.append(link)
                            '''d=get(link).text
                            s=BeautifulSoup(d,'lxml')
                            y=s.find('span',{'data-reactid':"40"}).text
                            if(y=='Fund Family'):
                                y="N/A"'''
                            
                                
                        if(not(text.startswith('+') and not(text.startswith('-')))):
                            try:
                                l.append(text)
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
            alter_command=alter_command.format(l[2],"'"+l[5]+"'","'"+l[6]+"'","'"+l[0]+"'")
            cur.execute(alter_command)
            
            #uncomment this the first time you run this
            '''insert_command=insert_command="INSERT INTO Mutual_Funds values ({},{},{},{},{})".format("'"+l[0]+"'","'"+l[1]+"'",l[2],"'"+l[5]+"'","'"+l[6]+"'")
            cur.execute(insert_command)'''
            #print("done")
    offset+=100

for url in links:
	d=get(url).text
	s=BeautifulSoup(d,'lxml')
	y=s.find('span',{'data-reactid':"40"}).text
	if(y=='Fund Family'):
	    y="N/A"
	x=s.find("h1").text
	x=x[:x.find(" -")]
		# print(x,y)
	c="""update mutual_funds set category={} where fund_code={}""".format("'"+y+"'","'"+x+"'")
	cur.execute(c)