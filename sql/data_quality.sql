-- ============================================================
-- ECOMMERCE DATA PIPELINE
-- DATA QUALITY CHECKS
-- ============================================================


-- ============================================================
-- 1. DUPLICATE ORDER IDS
-- ============================================================

SELECT
    order_id,
    COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 2. NULL ORDER IDS
-- ============================================================

SELECT
    COUNT(*) AS null_order_ids
FROM orders
WHERE order_id IS NULL;


-- ============================================================
-- 3. NULL CUSTOMER IDS IN ORDERS
-- ============================================================

SELECT
    COUNT(*) AS null_customer_ids
FROM orders
WHERE customer_id IS NULL;


-- ============================================================
-- 4. NULL PRODUCT IDS IN ORDERS
-- ============================================================

SELECT
    COUNT(*) AS null_product_ids
FROM orders
WHERE product_id IS NULL;


-- ============================================================
-- 5. INVALID QUANTITIES
-- ============================================================

SELECT
    COUNT(*) AS invalid_quantities
FROM orders
WHERE quantity IS NULL
   OR quantity <= 0;


-- ============================================================
-- 6. INVALID UNIT PRICES
-- ============================================================

SELECT
    COUNT(*) AS invalid_unit_prices
FROM orders
WHERE unit_price IS NULL
   OR unit_price < 0;


-- ============================================================
-- 7. INVALID TOTAL AMOUNTS
-- ============================================================

SELECT
    COUNT(*) AS invalid_total_amounts
FROM orders
WHERE total_amount IS NULL
   OR total_amount < 0;


-- ============================================================
-- 8. INCORRECT ORDER TOTALS
-- ============================================================

SELECT
    order_id,
    quantity,
    unit_price,
    total_amount
FROM orders
WHERE ROUND(quantity * unit_price, 2)
      <> ROUND(total_amount, 2);


-- ============================================================
-- 9. ORPHANED CUSTOMER REFERENCES
-- ============================================================

SELECT
    o.order_id,
    o.customer_id
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- ============================================================
-- 10. ORPHANED PRODUCT REFERENCES
-- ============================================================

SELECT
    o.order_id,
    o.product_id
FROM orders o
LEFT JOIN products p
    ON o.product_id = p.product_id
WHERE p.product_id IS NULL;


-- ============================================================
-- 11. DUPLICATE CUSTOMER IDS
-- ============================================================

SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 12. CUSTOMERS WITH MISSING REQUIRED FIELDS
-- ============================================================

SELECT
    customer_id,
    first_name,
    last_name,
    email
FROM customers
WHERE first_name IS NULL
   OR last_name IS NULL
   OR email IS NULL;


-- ============================================================
-- 13. DUPLICATE CUSTOMER EMAILS
-- ============================================================

SELECT
    email,
    COUNT(*) AS duplicate_count
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;


-- ============================================================
-- 14. DUPLICATE PRODUCT IDS
-- ============================================================

SELECT
    product_id,
    COUNT(*) AS duplicate_count
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;


-- ============================================================
-- 15. PRODUCTS WITH INVALID PRICES
-- ============================================================

SELECT
    product_id,
    product_name,
    unit_price
FROM products
WHERE unit_price IS NULL
   OR unit_price < 0;


-- ============================================================
-- 16. PRODUCTS WITH MISSING NAMES
-- ============================================================

SELECT
    product_id,
    product_name
FROM products
WHERE product_name IS NULL
   OR TRIM(product_name) = '';


-- ============================================================
-- 17. CUSTOMERS WITH INVALID EMAIL FORMAT
-- ============================================================

SELECT
    customer_id,
    email
FROM customers
WHERE email IS NOT NULL
  AND email NOT LIKE '%@%';


-- ============================================================
-- 18. FUTURE ORDER DATES
-- ============================================================

SELECT
    order_id,
    order_date
FROM orders
WHERE order_date > CURRENT_DATE;


-- ============================================================
-- 19. ORDERS BEFORE CUSTOMER SIGNUP
-- ============================================================

SELECT
    o.order_id,
    o.order_date,
    c.customer_id,
    c.signup_date
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
WHERE o.order_date < c.signup_date;


-- ============================================================
-- 20. SUMMARY OF TABLE COUNTS
-- ============================================================

SELECT
    (SELECT COUNT(*) FROM customers) AS customers,
    (SELECT COUNT(*) FROM products) AS products,
    (SELECT COUNT(*) FROM orders) AS orders;
    