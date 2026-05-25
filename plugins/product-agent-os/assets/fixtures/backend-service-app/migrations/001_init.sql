-- Synthetic migration for backend-service-app.
create table synthetic_orders (
  id text primary key,
  status text not null
);

