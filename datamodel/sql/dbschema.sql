create schema customer360;

create table customer360.tblAccount(
id Int Primary key,
Name varchar(100) ,
AccountNumber varchar(20) UNIQUE NOT NULL,
AcctType varchar(100),
BillingStreet varchar(100),
BillingCity varchar(30),
BillingState varchar(10),
BillingPostalCode varchar(10),
Phone varchar(20),
Fax  varchar(20),
Email varchar(20)
);

create table customer360.tblContact(
id Int Primary key,
FirstName varchar(100) ,
LastName varchar(100) ,
Title varchar(100),
acctid int,
BillingStreet varchar(100),
BillingCity varchar(30),
BillingState varchar(10),
BillingPostalCode varchar(10),
Phone varchar(20),
Fax  varchar(20),
Email varchar(20),
CONSTRAINT account_acct_id_fkey FOREIGN KEY (acctid)
      REFERENCES customer360.tblAccount (id) MATCH SIMPLE
);

create table customer360.tblProductCategory(
id Int Primary key,
Name varchar(100) NOT NULL
);

create table customer360.tblProduct(
id Int Primary key,
Name varchar(100) NOT NULL,
categoryid int,
status varchar(20) DEFAULT 'Áctive',
price int NOT NULL,
CONSTRAINT category_id_fkey FOREIGN KEY (categoryid)
      REFERENCES customer360.tblProductCategory (id) MATCH SIMPLE
);

create table customer360.tblOrder(
id Int Primary key,
acctid int,
orderDate TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
amount int,
discount int,
total int,
status varchar(20) DEFAULT 'New',
CONSTRAINT account_acct_id_fkey FOREIGN KEY (acctid)
      REFERENCES customer360.tblAccount (id) MATCH SIMPLE
);

create table customer360.tblClickStream(
webid varchar(20) Not null,
datetime TIMESTAMP,
OS varchar(10),
browser varchar(10),
response_time_ms int,
product varchar(100),
url varchar(1000)
);
