\c invest

-- recommend by category

select company_id, company, open
from nse_stocks where sector=
				(select sector 
				from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id 
				group by sector having count(sector)= 
										(select max(c) 
										 from 
											(select sector, count(*) as c 
											 from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id 
											 group by sector order by c desc limit 1) as t)) order by open desc;


-- recommend by price

select company_id, company, open
from nse_stocks 
where open between 
	(select min(open)from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id) 
	and 
	(select max(open)from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id) 
	and sector=(select sector 
				from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id 
				group by sector having count(sector)= 
										(select max(c) 
										 from 
											(select sector, count(*) as c 
											 from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id 
											 group by sector order by c desc limit 1) as t)) order by open desc;


-- check price change
-- define threshold
select user_stocks.company_id 
from user_stocks join nse_stocks on user_stocks.company_id=nse_stocks.company_id
where ((last-close)/last)* 100 > 0.00001;

-- watchlist

select company_id,company, close, last, ((last-close)/last)*100 as change
from nse_stocks natural join watchlist
where user_id='Maanvi' and ((last-close)/last)*100 > 0.05;  

select company_id,company, close, last, ((last-close)/last)*100 as change
from nse_stocks natural join watchlist
where user_id='Maanvi' and ((last-close)/last)*100<0;


--filter by price and company

select company_id,company, open
from nse_stocks
where sector='Utilities' and open < 10;

-- networth calc
drop table networth;
create table networth(quantity numeric,price numeric,total numeric);

insert into networth
select  distinct quantity,close,quantity*close as total
from user_stocks inner join nse_stocks on user_stocks.company_id=nse_stocks.company_id
where user_id='Maanvi';

insert into networth
select  distinct quantity,buying_price,quantity*buying_price as total
from user_mutual_funds inner join mutual_funds on user_mutual_funds.fund_code=mutual_funds.fund_code
where user_id='Maanvi';

insert into networth
select distinct u.loan_balance,-1,u.loan_balance*(-1)
	from user_loan u,user_details d
	where u.user_id='Maanvi';
select * from networth;
select sum(total) from networth;
drop table networth;




