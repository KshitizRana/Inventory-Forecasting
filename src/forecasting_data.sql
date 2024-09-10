SELECT 
    a.timestamp,
    a.product_id,
    a.estimated_stock_pct,
    a.category,
    a.unit_price,
    b.quantity,
    c.temperature
FROM stock_processed a
LEFT JOIN sales_processed b
    ON a.product_id = b.product_id AND a.timestamp = b.timestamp
LEFT JOIN temp_processed c
    ON a.timestamp = c.timestamp;
