DROP TABLE people;
DROP TABLE drive_licence;
DROP TABLE driving_condition;
DROP TABLE Restriction;
DROP TABLE vehicle_type;
DROP TABLE owner;
DROP TABLE auto_sale;
DROP TABLE ticket_type;
DROP TABLE ticket




CREATE TABLE people
(
	Social_IN INTEGER,
	name CHAR(20),
	height INTEGER,	
	weight INTEGER,
	eyecolor CHAR(20),
	haircolor CHAR(20),
	addr CHAR(50),
	gender CHAR(20),
	birthday CHAR(50),
);

CREATE TABLE drive_licence
(
	licence_no CHAR(20),	
	Social_IN INTEGER,
	class CHAR(20),
	photo CHAR(20),
	issuing_date CHAR(50),
	expiring_date CHAR(50),
);

CREATE TABLE driving_condition
(
	c_id INTEGER,
	description CHAR(100),
);

CREATE TABLE Restriction
(
	licence_no CHAR(20),
	r_id INTEGER,
);

CREATE TABLE vehicle_type
(
	type_id INTEGER,
	type_* CHAR(20),
);

CREATE TABLE vehicle
(
	serial_no INTEGER,
	maker CHAR(20),	
	model CHAR(20),
	year INTEGER,	
	color CHAR(20),
	type_id INTEGER,
);

CREATE TABLE owner
(
	onwer_id INTEGER,
	vehicle_id INTEGER,
	is_primary_owner CHAR(20),
);

CREATE TABLE auto_sale
(
	transaction_id INTEGER,
	seller_id INTEGER,
	buyer_id INTEGER,
	vehicle_id INTEGER,
	s_date, CHAR(50),	
	price CHAR(20),
);

CREATE TABLE ticket_type
(
	vtype CHAR(20),
	fine CHAR(20),
);

CREATE TABLE ticket
(
	ticket_no INTEGER,
	violator_no INTEGER,	
	vehicle_no CHAR(20),	
	office_no INTEGER,
	vtype CHAR(20),
	vdate CHAR(20),
	place CHAR(50),
	descriptions CHAR(100),
);
	
	
	

