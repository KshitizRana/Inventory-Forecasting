SELECT 
    a.timestamp,
    a.product_id,
    a.estimated_stock_pct,
    a.category,
    a.unit_price,
    b.quantity,
    c.temperature
FROM stocklevel_agg a
LEFT JOIN sales_agg b
    ON a.product_id = b.product_id AND a.timestamp = b.timestamp
LEFT JOIN stocktemp_agg c
    ON a.timestamp = c.timestamp;
