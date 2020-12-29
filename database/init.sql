CREATE DATABASE shippingChallenge;
USE shippingChallenge;

CREATE TABLE User
(
	userId int not null,
	surname varchar(255) not null,
	constraint User_pk
		primary key (userId)
);

INSERT INTO User (userId, surname) VALUES (1, "Robin");