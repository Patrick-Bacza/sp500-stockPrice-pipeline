CREATE TABLE daily_stock_prices (
	id SERIAL PRIMARY KEY,
	date DATE,
	ticker VARCHAR(5),
	open_price FLOAT,
	close_price FLOAT,
	volume VARCHAR,
	previous_close FLOAT,
	intraday_low FLOAT,
	intraday_high FLOAT,
	bid_price FLOAT,
	ask_price FLOAT



)

drop table test