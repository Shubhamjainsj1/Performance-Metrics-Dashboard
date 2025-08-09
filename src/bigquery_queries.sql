-- src/bigquery_queries.sql

-- 1) Create a view for daily KPIs
CREATE OR REPLACE VIEW `your-gcp-project-id.performance_dashboard.daily_kpis` AS
SELECT
  DATE(order_ts) AS date,
  city,
  COUNT(DISTINCT order_id) AS total_orders,
  AVG(order_value) AS avg_order_value,
  AVG(pickup_to_drop_mins) AS avg_delivery_mins,
  AVG(rating) AS avg_rating,
  SUM(incentive) AS total_incentive,
  SAFE_DIVIDE(SUM(on_time), COUNT(1)) AS on_time_rate
FROM `your-gcp-project-id.performance_dashboard.orders`
GROUP BY date, city;

-- 2) Agent-level summary
CREATE OR REPLACE VIEW `your-gcp-project-id.performance_dashboard.agent_summary` AS
SELECT
  agent_id,
  COUNT(DISTINCT order_id) AS orders_completed,
  AVG(pickup_to_drop_mins) AS avg_delivery_mins,
  AVG(rating) AS avg_rating,
  SUM(incentive) AS total_incentive,
  SAFE_DIVIDE(SUM(on_time), COUNT(1)) AS on_time_rate
FROM `your-gcp-project-id.performance_dashboard.orders`
GROUP BY agent_id;

-- 3) Month-over-month KPI view (example)
CREATE OR REPLACE VIEW `your-gcp-project-id.performance_dashboard.monthly_kpis` AS
SELECT
  FORMAT_TIMESTAMP('%Y-%m', TIMESTAMP_TRUNC(order_ts, MONTH)) AS month,
  COUNT(*) AS total_orders,
  AVG(order_value) AS avg_order_value,
  AVG(pickup_to_drop_mins) AS avg_delivery_mins
FROM `your-gcp-project-id.performance_dashboard.orders`
GROUP BY month
ORDER BY month;
