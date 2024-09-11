SELECT 
    s.*
    sl.product_id,
    sl.quantity,
    TEMP.temperature,
    sl.estimated_stock_pct,
FROM stocklevel_agg sl
LEFT JOIN sales_agg s ON sl.TIMESTAMP = s.TIMESTAMP
	AND sl.product_id = s.product_id
LEFT JOIN stocktemp_agg TEMP ON sl.TIMESTAMP = TEMP.TIMESTAMP;
