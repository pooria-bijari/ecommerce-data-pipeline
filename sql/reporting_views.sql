-- ============================================================
-- ECOMMERCE DATA PIPELINE
-- REPORTING VIEWS
-- ============================================================


-- ============================================================
-- 1. MONTHLY REVENUE
-- ============================================================

DROP VIEW IF EXISTS vw_monthly_revenue;

CREATE VIEW vw_monthly_revenue AS

SELECT
    DATE_TRUNC('month', order_date) AS month,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS revenue,
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY month;


-- ============================================================
-- 2. PRODUCT PERFORMANCE
-- ============================================================

DROP VIEW IF EXISTS vw_product_performance;

CREATE VIEW vw_product_performance AS

SELECT
    p.product_id,
    p.product_name,
    p.category,
    COUNT(o.order_id) AS number_of_orders,
    COALESCE(SUM(o.quantity), 0) AS units_sold,
    COALESCE(SUM(o.total_amount), 0) AS revenue,
    ROUND(
        COALESCE(AVG(o.total_amount), 0),
        2
    ) AS average_order_value
FROM products p
LEFT JOIN orders o
    ON p.product_id = o.product_id
GROUP BY
    p.product_id,
    p.product_name,
    p.category;


-- ============================================================
-- 3. CUSTOMER PERFORMANCE
-- ============================================================

DROP VIEW IF EXISTS vw_customer_performance;

CREATE VIEW vw_customer_performance AS

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.country,
    c.signup_date,
    COUNT(o.order_id) AS total_orders,
    COALESCE(SUM(o.quantity), 0) AS total_units,
    COALESCE(SUM(o.total_amount), 0) AS total_spent,
    ROUND(
        COALESCE(AVG(o.total_amount), 0),
        2
    ) AS average_order_value
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.country,
    c.signup_date;


-- ============================================================
-- 4. COUNTRY PERFORMANCE
-- ============================================================

DROP VIEW IF EXISTS vw_country_performance;

CREATE VIEW vw_country_performance AS

SELECT
    c.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.quantity) AS units_sold,
    SUM(o.total_amount) AS revenue,
    ROUND(
        AVG(o.total_amount),
        2
    ) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.country;


-- ============================================================
-- 5. DAILY SALES
-- ============================================================

DROP VIEW IF EXISTS vw_daily_sales;

CREATE VIEW vw_daily_sales AS

SELECT
    order_date,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    SUM(total_amount) AS revenue,
    ROUND(
        AVG(total_amount),
        2
    ) AS average_order_value
FROM orders
GROUP BY order_date;