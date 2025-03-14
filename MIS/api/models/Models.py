from enum import Enum
from typing import Optional
from .BaseModel import Model ,Field,FieldType,db


class ProductCategory(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name =  Field(FieldType.STRING)

    _table_name="prca"

class ProductGroup(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    Name =  Field(FieldType.STRING)

    _table_name="prgr"

class ProductBrand(Model):

    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    Name =  Field(FieldType.STRING)

    _table_name="prbr"


class SKU(Model):

    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    Name =  Field(FieldType.STRING)

    prgrCode =  Field(FieldType.STRING)
    BrandCode =  Field(FieldType.STRING)
    PriceRevisionLimit =  Field(FieldType.STRING)
    # Name =  Field(FieldType.STRING)

    _table_name="SKU"

class ZeroStockSKU(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    SlNo = Field(FieldType.INTEGER)

    SKUCode = Field(FieldType.INTEGER)
    DOT = Field(FieldType.DATE)
    PhysicalStock = Field(FieldType.INTEGER)
    LoginRef = Field(FieldType.STRING)


    _table_name="ZeroStockSKU"



class SalesLoss(Model):
    
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    SKUCode = Field(FieldType.INTEGER)
    Reason = Field(FieldType.STRING)
    DateFrom = Field(FieldType.DATE)
    DateTo = Field(FieldType.DATE)
    IsActive = Field(FieldType.INTEGER)
    LoginRef = Field(FieldType.STRING)
    ASM = Field(FieldType.INTEGER)
    ASPD = Field(FieldType.INTEGER)

    _table_name="SalesLoss"



class SKUSales(Model):

    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    SKUCode = Field(FieldType.INTEGER)
    DOT = Field(FieldType.DATE)
    qty = Field(FieldType.INTEGER)
    COGS = Field(FieldType.STRING)
    GrossAmount = Field(FieldType.STRING)

    _table_name="SKUSales"


class Sales(Model):
    code =  Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    DOT = Field(FieldType.DATE)
    GrossAmt = Field(FieldType.INTEGER)
    CardHolderCode =Field(FieldType.INTEGER)
    InvoiceNo =Field(FieldType.INTEGER)

    _table_name = "Sales"



class PriceRevision(Model):

    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    DOT = Field(FieldType.DATE)
    SKUCode = Field(FieldType.INTEGER)
    Rate = Field(FieldType.INTEGER)
    
    SalesPrice = Field(FieldType.INTEGER)
    PreviousSalesPrice = Field(FieldType.INTEGER)

    _table_name="PriceRevision"






class Customers(Model):

    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name = Field(FieldType.STRING,nullable=False)
    Phone = Field(FieldType.STRING)
    dot = Field(FieldType.DATE)
    LastSalesDate = Field(FieldType.DATE)

    NOB = Field(FieldType.INTEGER)
    ABV = Field(FieldType.INTEGER) #average bill value
    ABVMth = Field(FieldType.INTEGER)

    # ATV = Field(FieldType.INTEGER) #average store visit to be included 

    BillDaysFrom = Field(FieldType.INTEGER)
    BillDaysTo = Field(FieldType.INTEGER)

    Status = Field(FieldType.STRING)

    _table_name="Customers"


class ActiveCustomers(Model):
    CardHolderCode = Field(FieldType.STRING,is_primary=True,nullable=False)
    OCT = Field(FieldType.INTEGER)
    NOV = Field(FieldType.INTEGER)
    DEC = Field(FieldType.INTEGER)
    JAN = Field(FieldType.INTEGER)
    FEB = Field(FieldType.INTEGER)
    AMOUNT = Field(FieldType.INTEGER)

    _table_name = "ActiveCustomers"



class Users(Model):

    code  = Field(FieldType.INTEGER,is_primary=True,nullable=False)

    _table_name="Users"


class AccAuditCrNoteCashRefundDetails(Model):

    code = Field(FieldType.INTEGER,is_primary=True,nullable=False)
    dot = Field(FieldType.DATE)
    entryDate = Field(FieldType.DATE)
    VoucherNo = Field(FieldType.INTEGER)
    Description = Field(FieldType.STRING)
    AccountName = Field(FieldType.STRING)
    Amount = Field(FieldType.INTEGER)
    Termina = Field(FieldType.STRING) #change typo
    PostedBy = Field(FieldType.STRING)
    BackDatedDays = Field(FieldType.INTEGER)

    _table_name = 'AccAuditCrNoteCashRefundDetails'

class AccAuditCrNoteCashRefundSummary(Model):
    dot = Field(FieldType.DATE)
    Amount = Field(FieldType.INTEGER)
    Termina = Field(FieldType.STRING)
    PostedBy = Field(FieldType.STRING)

    _table_name = 'AccAuditCrNoteCashRefundSummary'

class AccAuditExpAsIncome(Model):

    code = Field(FieldType.INTEGER,is_primary=True,nullable=False)
    dot = Field(FieldType.DATE)
    VoucherNo = Field(FieldType.INTEGER)
    Description = Field(FieldType.STRING)
    Account = Field(FieldType.STRING)
    DrAmout = Field(FieldType.INTEGER)
    CrAmout = Field(FieldType.INTEGER)

    _table_name = 'AccAuditExpAsIncome'

class AccAuditRange(Model):

    code = Field(FieldType.INTEGER,is_primary=True,nullable=False)
    DOT = Field(FieldType.DATE)
    VoucherNo = Field(FieldType.INTEGER)
    Amount = Field(FieldType.STRING)
    Name = Field(FieldType.STRING)
    Amount = Field(FieldType.INTEGER)
    Mode = Field(FieldType.INTEGER)
    Description = Field(FieldType.STRING)
    accGroup = Field(FieldType.STRING)
    LedgerCode = Field(FieldType.INTEGER)

    _table_name = 'AccAuditRange'

class ActiveCustomers(Model):
    CardHolderCode = Field(FieldType.INTEGER,nullable=False,is_primary=True)

    OCT = Field(FieldType.INTEGER,nullable=False)
    NOV = Field(FieldType.INTEGER,nullable=False)
    DEC = Field(FieldType.INTEGER,nullable=False)
    JAN = Field(FieldType.INTEGER,nullable=False)
    FEB = Field(FieldType.INTEGER,nullable=False)
    AMOUNT = Field(FieldType.INTEGER)
    NPC = Field(FieldType.INTEGER)

    _table_name = 'ActiveCustomers'

class BackDatedAccounts(Model):
    CODE = Field(FieldType.INTEGER,nullable=False,is_primary=True)
    DOT = Field(FieldType.DATE)
    EntryDate = Field(FieldType.DATE,nullable=False)
    VoucherNo = Field(FieldType.INTEGER,nullable=False)
    Description = Field(FieldType.STRING)
    TransName = Field(FieldType.STRING)
    Name = Field(FieldType.STRING)
    Dr = Field(FieldType.INTEGER)
    Cr = Field(FieldType.INTEGER)
    Alias = Field(FieldType.STRING)
    caCode = Field(FieldType.INTEGER)

    _table_name= 'BackDatedAccounts'

class LiveCustomerData(Model):   #last two month customer data
    Code = Field(FieldType.INTEGER,nullable=False,is_primary=True)
    Name = Field(FieldType.STRING)
    cardholdercode = Field(FieldType.INTEGER)
    Last2MthSales = Field(FieldType.INTEGER)
    contribution = Field(FieldType.INTEGER)
    rank = Field(FieldType.INTEGER)
    cumulativeTotal = Field(FieldType.INTEGER)
    cumulativeContribution = Field(FieldType.INTEGER)
    LowSales = Field(FieldType.INTEGER)
    cumulativeContributionPart = Field(FieldType.INTEGER)
    _table_name = "LiveCustomerData"

class StkZeroStockSku(Model):
    code = Field(FieldType.INTEGER)
    SkuName = Field(FieldType.STRING)
    CQTY = Field(FieldType.INTEGER)

    GroupName = Field(FieldType.STRING)
    pwSales = Field(FieldType.INTEGER)
    D7 = Field(FieldType.INTEGER)
    D6 = Field(FieldType.INTEGER)
    D5 = Field(FieldType.INTEGER)
    D4 = Field(FieldType.INTEGER)
    D3 = Field(FieldType.INTEGER)
    D2 = Field(FieldType.INTEGER)
    D1 = Field(FieldType.INTEGER)
    cuWSales	 = Field(FieldType.INTEGER)
    pwSQty	 = Field(FieldType.INTEGER)
    cwSQty	 = Field(FieldType.INTEGER)


















    