-- Find missing amounts
SELECT * FROM transactions WHERE amount IS NULL;

-- Find negative amounts
SELECT * FROM transactions WHERE amount < 0;

-- Find duplicate transactions
SELECT transaction_id, COUNT(*) 
FROM transactions 
GROUP BY transaction_id
HAVING COUNT(*) > 1;

-- Validate dates
SELECT * FROM transactions 
WHERE TRY_CAST(date AS DATE) IS NULL;
