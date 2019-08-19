create schema IF NOT EXISTS customer360;
set search_path to customer360;

drop table if exists tblSupportTicket,tblClickStream,tblOrder,tblProduct,tblProductCategory,tblContact,tblAccount;

create table tblAccount(
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
Email varchar(100),
Status varchar(20) DEFAULT 'ActiveCustomer'
);

create table tblContact(
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
CONSTRAINT account_acct_id_fkey FOREIGN KEY (acctid)
      REFERENCES customer360.tblAccount (id) MATCH SIMPLE
);

create table tblProductCategory(
id Int Primary key,
Name varchar(100) NOT NULL
);

create table tblProduct(
id Int Primary key,
Name varchar(100) NOT NULL,
categoryid int,
status varchar(20) DEFAULT 'Áctive',
price int NOT NULL,
profitMarginpct int NOT NULL,
CONSTRAINT category_id_fkey FOREIGN KEY (categoryid)
      REFERENCES customer360.tblProductCategory (id) MATCH SIMPLE
);

create table tblOrder(
id Int Primary key,
acctid int,
orderDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
amount int,
discount int,
status varchar(20) DEFAULT 'New',
CONSTRAINT account_acct_id_fkey FOREIGN KEY (acctid)
      REFERENCES customer360.tblAccount (id) MATCH SIMPLE
);

create table tblClickStream(
webid varchar(20) Not null,
datetime TIMESTAMP,
OS varchar(10),
browser varchar(10),
response_time_ms int,
product varchar(100),
url varchar(1000)
);

create table tblClickStreamWithAcctIDMatch(
webid varchar(20) Not null,
acctid int,
datetime TIMESTAMP,
OS varchar(10),
browser varchar(10),
response_time_ms int,
product varchar(100),
url varchar(1000)
);

create table tblSupportTicket(
ticketnumber Int Primary Key,
creatorID Int,
datetime TIMESTAMP,
status varchar(20) DEFAULT 'New',
description varchar(1000),
attachments varchar(1000),
initialResponse TIMESTAMP,
closeDate TIMESTAMP,
feedback varchar(1000),
CONSTRAINT contact_id_fkey FOREIGN KEY (creatorID)
      REFERENCES customer360.tblContact (id) MATCH SIMPLE
);


create table tblCustomerOrderAnalytics(
acctid int,
yr int,
quarter int,
numorders int,
grosstotal int,
avgdiscount int
);

create table tblCustomerOrderStatusAnalytics(
acctid int,
yr int,
quarter int,
orderstatus varchar(20),
numorders int
);

create table tblCustomerClickStreamAnalytics(
acctid int,
yr int,
mm int,
visits int
)
