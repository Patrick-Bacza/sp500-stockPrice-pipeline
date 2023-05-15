CREATE TABLE companies (
	Ticker VARCHAR(6) PRIMARY KEY,
	Company VARCHAR,
	Sector_id CHAR(4),
	Industry_id CHAR(4),
	FOREIGN KEY (Sector_id) REFERENCES sectors (sector_id),
	FOREIGN KEY (Industry_id) REFERENCES industries (Industry_id)
	
)

CREATE TABLE sectors (
	Sector_id VARCHAR(4) PRIMARY KEY,
	Sector VARCHAR

)

CREATE TABLE industries (
	Industry_id VARCHAR(4) PRIMARY KEY,
	Industry VARCHAR,
	Sector_id VARCHAR,
	FOREIGN KEY (Sector_id) REFERENCES sectors (Sector_id)
	
)


SELECT 
	*
FROM 
	companies c
JOIN 
	sectors s
ON
	c.sector_id = s.sector_id
JOIN industries i

ON 
	i.industry_id = c.industry_id
	


