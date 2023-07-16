CREATE TABLE daily_stock_prices (
	id SERIAL PRIMARY KEY,
	date DATE,
	ticker VARCHAR(11),
	open_price FLOAT,
	close_price FLOAT,
	volume BIGINT,
	previous_close FLOAT,
	intraday_low FLOAT,
	intraday_high FLOAT,
)

