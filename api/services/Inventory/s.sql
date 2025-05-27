select * from LiveSku

    select pg.code,pg.name,l.SkuName,tm.GrossAmt
     from GroupNbrands gb,productGroups pg,LiveSku l,skuSalesThisMonth tm where gb.ProductGroupCode=pg.Code
    and l.GroupNBrandCode=gb.Code and tm.UbDetailsCode=l.code


select pg.code,pg.name,sum(tm.GrossAmt) amt
     from GroupNbrands gb,productGroups pg,LiveSku l,skuSalesThisMonth tm where gb.ProductGroupCode=pg.Code
     and l.GroupNBrandCode=gb.Code and tm.UbDetailsCode=l.code
group by pg.code,pg.Name order by pg.Name


-------------------sku. gbCode
  gb...productgroupcode,productbrandcode    --- groupname,brandname(old)

  ----------- productGroups
--
