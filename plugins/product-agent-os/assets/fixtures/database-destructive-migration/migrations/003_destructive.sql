DROP TABLE legacy_orders;
TRUNCATE TABLE staging_orders;
ALTER TABLE orders RENAME TO orders_old;
