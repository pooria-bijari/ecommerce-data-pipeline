-- ============================================================
-- ECOMMERCE DATA PIPELINE
-- ANALYTICS QUERIES
-- ============================================================


-- ============================================================
-- 1. OVERALL BUSINESS METRICS
-- ============================================================

SELECT
    COUNT(*) AS total_orders,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value,
    MIN(total_amount) AS smallest_order,
    MAX(total_amount) AS largest_order
FROM orders;


-- ============================================================
-- 2. TOTAL REVENUE
-- ============================================================

SELECT
    SUM(total_amount) AS total_revenue
FROM orders;


-- ============================================================
-- 3. TOTAL NUMBER OF ORDERS
-- ============================================================

SELECT
    COUNT(*) AS total_orders
FROM orders;


-- ============================================================
-- 4. AVERAGE ORDER VALUE
-- ============================================================

SELECT
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders;


-- ============================================================
-- 5. MONTHLY REVENUE
-- ============================================================

SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;


-- ============================================================
-- 6. DAILY REVENUE
-- ============================================================

SELECT
    order_date,
    COUNT(*) AS total_orders,
    SUM(total_amount) AS revenue
FROM orders
GROUP BY order_date
ORDER BY order_date;


-- ============================================================
-- 7. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.total_amount) AS revenue,
    SUM(o.quantity) AS units_sold
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC
LIMIT 10;


-- ============================================================
-- 8. REVENUE BY PRODUCT CATEGORY
-- ============================================================

SELECT
    p.category,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS revenue,
    ROUND(AVG(o.total_amount), 2) AS average_order_value
FROM orders o
JOIN products p
    ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue DESC;


-- ============================================================
-- 9. TOP 10 CUSTOMERS BY SPENDING
-- ============================================================

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS total_spent,
    ROUND(AVG(o.total_amount), 2) AS average_order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country
ORDER BY total_spent DESC
LIMIT 10;


-- ============================================================
-- 10. REVENUE BY COUNTRY
-- ============================================================

SELECT
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS revenue,
    ROUND(AVG(o.total_amount), 2) AS average_order_value
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY c.country
ORDER BY revenue DESC;


-- ============================================================
-- 11. TOP 10 CUSTOMERS BY NUMBER OF ORDERS
-- ============================================================

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.country,
    COUNT(o.order_id) AS number_of_orders,
    SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country
ORDER BY number_of_orders DESC
LIMIT 10;


-- ============================================================
-- 12. HIGHEST-VALUE ORDERS
-- ============================================================

SELECT
    o.order_id,
    o.order_date,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    p.product_name,
    o.quantity,
    o.unit_price,
    o.total_amount
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN products p
    ON o.product_id = p.product_id
ORDER BY o.total_amount DESC
LIMIT 20;


-- ============================================================
-- 13. CUSTOMER PURCHASE FREQUENCY
-- ============================================================

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.country,
    COUNT(o.order_id) AS number_of_orders,
    COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country
ORDER BY number_of_orders DESC;


-- ============================================================
-- 14. PRODUCT PERFORMANCE
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS number_of_orders,
    COALESCE(SUM(o.quantity), 0) AS units_sold,
    COALESCE(SUM(o.total_amount), 0) AS revenue,
    ROUND(COALESCE(AVG(o.total_amount), 0), 2) AS average_order_value
FROM products p
LEFT JOIN orders o
    ON p.product_id = o.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue DESC;


-- ============================================================
-- 15. SALES QUANTITY BY PRODUCT
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY units_sold DESC;


-- ============================================================
-- 16. REVENUE PER UNIT
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS revenue,
    ROUND(
        SUM(o.total_amount) / NULLIF(SUM(o.quantity), 0),
        2
    ) AS revenue_per_unit
FROM products p
JOIN orders o
    ON p.product_id = o.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category
ORDER BY revenue_per_unit DESC;


-- ============================================================
-- 17. CUSTOMER LIFETIME VALUE
-- ============================================================

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country
ORDER BY lifetime_value DESC;


-- ============================================================
-- 18. MONTHLY UNITS SOLD
-- ============================================================

SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;


-- ============================================================
-- 19. CUSTOMER ACQUISITION BY SIGNUP MONTH
-- ============================================================

SELECT
    DATE_TRUNC('month', signup_date) AS signup_month,
    COUNT(customer_id) AS new_customers
FROM customers
GROUP BY DATE_TRUNC('month', signup_date)
ORDER BY signup_month;


-- ============================================================
-- 20. PRODUCTS WITH NO SALES
-- ============================================================

SELECT
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price
FROM products p
LEFT JOIN orders o
    ON p.product_id = o.product_id
WHERE o.order_id IS NULL
ORDER BY p.product_id;