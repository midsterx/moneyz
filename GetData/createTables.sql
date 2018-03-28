
-- drop table nse_stocks;
CREATE TABLE nse_stocks (
    company varchar(200),
    company_id varchar(100),
    timestamp_d date,
    open numeric,
    high numeric,
    low numeric,
    last numeric, 
    close numeric,
    total_trade_qty numeric,
    turnover numeric,
    sector varchar(50),
    industry varchar(50),
    primary key (company_id) 
);
-- drop table mutual_funds;
CREATE TABLE mutual_funds (
    fund_code varchar(20),
    fund_name varchar(100),
    timestamp_d date,
    price numeric,
    three_mo_return varchar(10),
    ytd_ret varchar(10),
    category varchar(50),
    primary key (fund_code) 
);
-- drop table timeseries_stocks;
CREATE TABLE timeseries_stocks (
	company_id varchar(100),
	price numeric,
	timestamp_d date unique,
	primary key (company_id,timestamp_d)
);
-- drop table timeseries_mutual_fund;
CREATE TABLE timeseries_mutual_fund (
    fund_code varchar(20),
    price numeric,
    timestamp_d date unique,
    primary key (fund_code,timestamp_d)
);
-- drop table user_details;
CREATE TABLE user_details (
    user_id varchar(20),
    email_address varchar(20),
    password varchar(20),
    primary key(user_id) 
);
-- drop table user_loan;
CREATE TABLE user_loan (
	user_id varchar(20),
	loan_type varchar(50),
	loan_amount numeric,
	start_date date,
	tenure numeric(2,0),
	loan_balance numeric,
	interest_paid numeric,
	principal_paid numeric,
	EMIs_to_pay numeric,
	bank_name varchar(50),
	foreign key(user_id) references user_details(user_id),
	primary key(user_id,start_date,bank_name)
);
-- drop table user_stocks;
CREATE TABLE user_stocks (
    user_id varchar(20) ,
    company_id varchar(100),
    timestamp_d date not null,
    buying_price numeric not null,
    quantity numeric not null,
    foreign key(user_id) references user_details(user_id),
    foreign key(company_id) references nse_stocks(company_id),
    primary key(user_id,company_id,timestamp_d)
);
-- drop table user_mutual_fund;

CREATE TABLE user_mutual_funds (
	user_id varchar(20),
	fund_code varchar(20),
	timestamp_d date,
	buying_price numeric,
	quantity numeric,
	foreign key(user_id) references user_details(user_id),
	foreign key(fund_code) references mutual_funds(fund_code),
    primary key(user_id, fund_code,timestamp_d)
);
