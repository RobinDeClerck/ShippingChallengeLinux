CREATE DATABASE shippingChallenge;
USE shippingChallenge;

CREATE TABLE User
(
	userId int auto_increment,
	surname varchar(255) null,
	constraint User_pk
		primary key (userId)
);

INSERT INTO User (surname) VALUES ("Robin");