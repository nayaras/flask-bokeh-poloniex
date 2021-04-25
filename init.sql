CREATE DATABASE IF NOT EXISTS smarttbot;
USE smarttbot;
CREATE TABLE IF NOT EXISTS cotacao(
	id INT AUTO_INCREMENT PRIMARY KEY,
	moeda_label VARCHAR(100),
	moeda_cod VARCHAR(100),
	periodicidade VARCHAR(10),
	data_hora DATETIME,
	open DOUBLE,
	low DOUBLE,
	high DOUBLE,
	close DOUBLE
);