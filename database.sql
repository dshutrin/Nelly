CREATE DATABASE assistant;
CREATE USER 'assist_user'@'%' IDENTIFIED BY 'assist_password';
REVOKE ALL PRIVILEGES ON *.* FROM 'assist_user'@'%';
GRANT SELECT ON assistant.* TO 'assist_user'@'%' WITH GRANT OPTION;
FLUSH PRIVILEGES;

USE assistant;
CREATE TABLE variables(
	phrase VARCHAR(100),
	func VARCHAR(100)
);
