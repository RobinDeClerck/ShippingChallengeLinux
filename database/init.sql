CREATE DATABASE ShippingChallenge;
USE ShippingChallenge;

CREATE TABLE User
(
	userId int not null,
	surname varchar(255) not null,
	constraint User_pk1
		primary key (userId)
);

INSERT INTO User (userId, surname) VALUES (1, "Robin");