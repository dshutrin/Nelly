CREATE DATABASE assistant;
CREATE USER 'assist_user'@'%' IDENTIFIED BY 'assist_password';
REVOKE ALL PRIVILEGES ON *.* FROM 'assist_user'@'%';
GRANT ALL PRIVILEGES ON assistant.* TO 'assist_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

USE assistant;

/* Таблица для соотношений фразы и функции */
CREATE TABLE variables(
	phrase VARCHAR(100),
	func VARCHAR(100)
);

/* Таблица для системных параметров ассистента */
CREATE TABLE system_data(
	param VARCHAR(100),
	value VARCHAR(100)
);
