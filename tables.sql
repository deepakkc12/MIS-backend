

CREATE TABLE prca(
Code numeric primary key identity(1,1),
Name varchar(250)
);

CREATE TABLE prgr(
Code  numeric primary key identity(1,1),
Name varchar(250),
CategoryCode numeric foreign key references prca(Code)
);

CREATE TABLE prbr(
Code numeric primary key identity(1,1),
Name varchar(250)
);

CREATE TABLE SKU(

Code numeric primary key identity(1,1),
Name varchar (250),
prgrCode numeric foreign key references prgr(Code),
BrandCode numeric Foreign key References prbr(Code),
PriceRevisionLimit decimal(10,4)

);

CREATE TABLE ZeroStockSKU(

Code numeric primary key identity(1,1),
SlNo numeric,
SKUCode numeric foreign key references SKU(Code),
DOT Date,
PhysicalStock numeric,
LoginRef text

);

CREATE TABLE SalesLoss(

Code numeric primary key identity(1,1),
SKUCode numeric foreign key references SKU(Code),
Reason text,
DateFrom Date,
DateTo Date,
IsActive int,
LoginRef text,
ASM int, ---avg sales margin
ASPD int ---avg sales per day

);

CREATE TABLE SKUSales(
Code numeric primary key identity(1,1),
DOT date,
qty numeric,
COGS numeric,
GrossAmount decimal(10,4),
SKUCode numeric
Foreign key References SKU(Code)
);

CREATE TABLE PriceRevision(
Code numeric primary key identity(1,1),
DOT Date,
SKUCode numeric foreign key References SKU(Code),
Rate decimal(10,4),
SalesPrice decimal(10,4),
PreviousSalesPrice decimal(10,4)
);

CREATE TABLE Customers(
    Code numeric primary key identity(1,1),
    DOT Date,
    MobileNo text,
    ABV decimal(10,4),
    ATV decimal(10,4),
    LastVisited Date,
    CardNo text

)