-------------  Creating Database  -----------------

CREATE DATABASE Egypt_Sales_Analysis_DB;

USE Egypt_Sales_Analysis_DB

-------------  KPIs  -----------------

SELECT 
ROUND(SUM((Quantity - ReturnQuantity) * UnitListPrice * ( 1 - Dis_Rate)), 2) AS NetSalesAfterReturns,
ROUND(SUM(TotalCost - (ISNULL(ReturnQuantity, 0) * UnitCost)), 2) AS NetCost,
ROUND(
    SUM((NetSalesAmount - ISNULL(ReturnAmount, 0)) 
        - (TotalCost - (ISNULL(ReturnQuantity, 0) * UnitCost))), 2) AS NetProfit,
ROUND(
    SUM((NetSalesAmount - ISNULL(ReturnAmount, 0)) 
        - (TotalCost - (ISNULL(ReturnQuantity, 0) * UnitCost))) * 100.0
    / SUM(NetSalesAmount - ISNULL(ReturnAmount, 0)),2) AS ProfitMarginPercent
FROM FactSales
WHERE OrderStatus <> 'Cancelled';


---------------- Monthly Sales ----------------

SELECT 
YEAR (OrderDate) AS OrderYear,
MONTH (OrderDate) as OrderMonth,
ROUND(SUM(NetSalesAmount - ISNULL(ReturnAmount, 0)), 2) AS NetSalesAfterReturns
FROM FactSales
WHERE OrderStatus <> 'Cancelled'
GROUP BY
year(OrderDate),
MONTH (OrderDate)
ORDER BY
OrderYear,
OrderMonth