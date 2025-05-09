from enum import Enum
from typing import Optional
from .BaseModel import Model ,Field,FieldType,db


class GroupNbrands(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    prgrCode =Field(FieldType.INTEGER)
    brandCode =Field(FieldType.INTEGER)
    GroupName =Field(FieldType.STRING)
    BrandName =Field(FieldType.STRING)
    Grade =Field(FieldType.INTEGER)
    SalesRank =Field(FieldType.INTEGER)
    ProfitRank =Field(FieldType.INTEGER)
    Promoted =Field(FieldType.INTEGER)
    CloseWatch =Field(FieldType.INTEGER)
    ClusterCode =Field(FieldType.INTEGER)
    ProdcutCategoryCode =Field(FieldType.INTEGER)
    ProductSubCategoryCode =Field(FieldType.INTEGER)
    ProductGroupCode =Field(FieldType.INTEGER)
    ProductSubGroupCode =Field(FieldType.INTEGER)
    ProductBrandCode =Field(FieldType.INTEGER)
    perGramMax =Field(FieldType.INTEGER)
    perGramMin =Field(FieldType.INTEGER)

    _table_name = "GroupNbrands"

class productCategory(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name =  Field(FieldType.STRING)
    refCode =  Field(FieldType.STRING)

    _table_name="productCategory"

class productsubCategory(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name =  Field(FieldType.STRING)
    Category =  Field(FieldType.STRING)
    categoryCode =  Field(FieldType.STRING)

    _table_name="productsubCategory"

class productGroups(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name =  Field(FieldType.STRING)
    Category =  Field(FieldType.STRING)
    ProductCategoryCode =  Field(FieldType.STRING)
    convQtyRequired =Field(FieldType.INTEGER)
    convQtyAtSku =Field(FieldType.INTEGER)

    _table_name="productGroups"

class productSubGroup(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name =  Field(FieldType.STRING)
    GroupName =  Field(FieldType.STRING)
    productGroupCode =  Field(FieldType.INTEGER)

    _table_name="productSubGroup"

class LiveSku(Model):
    code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    SkuName =  Field(FieldType.STRING)
    Details =  Field(FieldType.STRING)
    cQty =  Field(FieldType.INTEGER)
    prgrCode =  Field(FieldType.INTEGER)
    brandCode =  Field(FieldType.INTEGER)
    PackingCode =  Field(FieldType.INTEGER)
    TaxGroupCode =  Field(FieldType.INTEGER)
    GroupNBrandCode =  Field(FieldType.INTEGER)
    recentPackUnit =  Field(FieldType.INTEGER)
    PackUnitRange1 =  Field(FieldType.INTEGER)
    PackUnitRange2 =  Field(FieldType.INTEGER)
    uom	 =  Field(FieldType.STRING)

    L1Choice =  Field(FieldType.INTEGER)
    L2Choice =  Field(FieldType.INTEGER)
    L3Choice =  Field(FieldType.INTEGER)
    L4Choice =  Field(FieldType.INTEGER)
    LowChoice =  Field(FieldType.INTEGER)
    L1ChoiceQty =  Field(FieldType.INTEGER)
    L2ChoiceQty =  Field(FieldType.INTEGER)
    L3ChoiceQty =  Field(FieldType.INTEGER)
    L4ChoiceQty =  Field(FieldType.INTEGER)

    LowChoiceQty =  Field(FieldType.INTEGER)

    _table_name = "LiveSku"

class LiveSubSKu(Model):
    code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    SubSkuName =  Field(FieldType.STRING)
    SkuName =  Field(FieldType.STRING)
    ConversionQty =  Field(FieldType.INTEGER)
    skuConvQty =  Field(FieldType.INTEGER)
    skuCode =  Field(FieldType.INTEGER)
    MRP =  Field(FieldType.INTEGER)
    SP1 =  Field(FieldType.INTEGER)
    SalesPrice2 =  Field(FieldType.INTEGER)
    SP3 =  Field(FieldType.INTEGER)
    PLU =  Field(FieldType.INTEGER)
    ismop =  Field(FieldType.INTEGER)

    HSN =  Field(FieldType.STRING)
    verified =  Field(FieldType.INTEGER)
    AutocQty =  Field(FieldType.INTEGER)


    _table_name = "LiveSubSku"

class productBrands(Model):
    Code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    Name =  Field(FieldType.STRING)

    _table_name = "productBrands"

class skuSalesPrevMonth(Model):
    UbDetailsCode = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    GrossAmt =  Field(FieldType.INTEGER)
    COGS =  Field(FieldType.INTEGER)
    Qty =  Field(FieldType.INTEGER)
    MRPTotal =  Field(FieldType.INTEGER)
    Discount =  Field(FieldType.INTEGER)
    GroupNBrandCode =  Field(FieldType.INTEGER)

    _table_name = "skuSalesPrevMonth"

class skuSalesThisMonth(Model):
    UbDetailsCode = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    GrossAmt =  Field(FieldType.INTEGER)
    COGS =  Field(FieldType.INTEGER)
    Qty =  Field(FieldType.INTEGER)
    MRPTotal =  Field(FieldType.INTEGER)
    Discount =  Field(FieldType.INTEGER)
    GroupNBrandCode =  Field(FieldType.INTEGER)

    _table_name = "skuSalesThisMonth"

class SkuStock(Model):
    ubDetailsCode = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    D7 =  Field(FieldType.INTEGER)
    D6 =  Field(FieldType.INTEGER)
    D5 =  Field(FieldType.INTEGER)
    D4 =  Field(FieldType.INTEGER)
    D3 =  Field(FieldType.INTEGER)
    
    D2 =  Field(FieldType.INTEGER)
    D1 =  Field(FieldType.INTEGER)
    pwSales =  Field(FieldType.INTEGER)
    cuWSales =  Field(FieldType.INTEGER)
    pwSQty =  Field(FieldType.INTEGER)
    cwSQty =  Field(FieldType.INTEGER)

    _table_name = "SkuStock"

class StkZeroStockSku(Model):
    code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    SkuName =  Field(FieldType.STRING)
    CQTY	 =  Field(FieldType.INTEGER)
    GroupName =  Field(FieldType.STRING)
    pwSales =  Field(FieldType.INTEGER)
    D7 =  Field(FieldType.INTEGER)
    D6 =  Field(FieldType.INTEGER)
    D5 =  Field(FieldType.INTEGER)
    D4 =  Field(FieldType.INTEGER)
    D3 =  Field(FieldType.INTEGER)
    D2 =  Field(FieldType.INTEGER)
    D1 =  Field(FieldType.INTEGER)
    cuWSales =  Field(FieldType.INTEGER)
    pwSQty =  Field(FieldType.INTEGER)
    cwSQty =  Field(FieldType.INTEGER)

    _table_name = "StkZeroStockSku"

class purchasePriceValidation(Model):
    
    code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)
    PTC =  Field(FieldType.INTEGER)
    PurchaseDate =  Field(FieldType.STRING)
    SkuName =  Field(FieldType.STRING)
    GroupName =  Field(FieldType.STRING)
    Vendor =  Field(FieldType.STRING)
    QTY =  Field(FieldType.INTEGER)
    Rate =  Field(FieldType.INTEGER)
    InwardRate =  Field(FieldType.INTEGER)
    previous_rate =  Field(FieldType.INTEGER)
    Per =  Field(FieldType.INTEGER)
    previous_dot =  Field(FieldType.STRING)
    inwardAge =  Field(FieldType.INTEGER)
    previous_Vendor =  Field(FieldType.INTEGER)
    dot =  Field(FieldType.DATE)

    _table_name = "purchasePriceValidation"

class SalesPriceValidation(Model):
    code = Field(FieldType.INTEGER,is_primary=True,auto_increment=False)

    PTC =  Field(FieldType.INTEGER)
    SkuName =  Field(FieldType.STRING)
    ismop =  Field(FieldType.INTEGER)
    dot =  Field(FieldType.DATE)
    MRP =  Field(FieldType.INTEGER)
    SP1 =  Field(FieldType.INTEGER)
    previous_mrp =  Field(FieldType.INTEGER)
    previous_SP1 =  Field(FieldType.INTEGER)
    previous_dot =  Field(FieldType.DATE)

    per =  Field(FieldType.INTEGER)
    GapDays =  Field(FieldType.INTEGER)
    GroupName =  Field(FieldType.INTEGER)

    _table_name = "SalesPriceValidation"




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
    CustomerLevel =Field(FieldType.INTEGER)
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





class StkBills(Model):

    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
    CODE = Field(FieldType.INTEGER,)
