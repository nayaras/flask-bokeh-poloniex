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

/*INSERT INTO cotacao (moeda_label, moeda_cod, periodicidade, data_hora, open, low, high, close) VALUES ('Bitcoin', 'USDT_BTC', '1', now(), '54633.59', '54687.82353358', '54659.18107648', '54633.59493125');
INSERT INTO cotacao (moeda_label, moeda_cod, periodicidade, data_hora, open, low, high, close) VALUES ('Bitcoin', 'USDT_BTC', '5', now(), '53770.50', '53792.77690559', '53770.50114211', '53770.50114212');
INSERT INTO cotacao (moeda_label, moeda_cod, periodicidade, data_hora, open, low, high, close) VALUES ('Bitcoin', 'USDT_BTC', '10', now(), '54841.00', '54852.00', '54848.97413428', '54848.97413428');
*/