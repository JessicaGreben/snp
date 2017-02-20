CREATE TABLE ohlcv (
  id SERIAL,
  date date,
  symbol VARCHAR(255),
  open NUMERIC(20, 2),
  high NUMERIC(20, 2),
  low NUMERIC(20, 2),
  close NUMERIC(20, 2),
  volume NUMERIC(20, 2),
  PRIMARY KEY (id)
);
