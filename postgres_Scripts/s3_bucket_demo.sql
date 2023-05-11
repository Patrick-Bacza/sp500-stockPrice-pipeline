CREATE EXTENSION aws_s3 CASCADE;

SELECT aws_s3.table_import_from_s3(
'test', 'date, ticker, open_price , close_price , volume , previous_close , intraday_low, intraday_high , bid_price , ask_price', '(format csv, header true)',
'dailystockprices',
'stock_prices/stock_prices_2023-05-10T16-50-49.csv',
'us-east-2',
'AKIAZEXWGFMGKEXRIWV6', 'n5i+3vH7vmLJ/nDPHQDRK1O9HYwDgL1+j0+1X3fZ'
)


select * FROM test
