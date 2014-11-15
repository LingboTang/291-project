INSERT into people values('10010010','Jack',175,60,'black','brown','9025-104ave,Edmonton Alberta','m','01-JAN-1970');
INSERT into people values('10010011','Tom',170,60,'brown','black','3214-111ave,La California','f','14-FEB-1978');
INSERT into people values('10010012','Frank',178,68,'blue','black','1666-98ave,Chengdu Sichuan','m','17-MAY-1988');
INSERT into people values('10010013','Dracky',164,55,'blue','Golden','1332-76ave,Edmonton Alberta','f','17-JUL-1992');
INSERT into people values('10010014','Drangon',184,80,'blue','Golden','3765-76ave,Edmonton Alberta','m','17-NOV-1994');
INSERT into people values('10010015','Laudi',182,80,'black','black','7725-90ave,Edmonton Alberta','m','09-OCT-1987');
INSERT into people values('10010016','SB',177,75,'browm','black','8293-56ave,Edmonton Alberta','m','27-FEB-1985');
INSERT into people values('10010017','Tamareial',185,85,'brown','brown','9023-111ave,Calgary Alberta','m','20-MAR-1986');
INSERT into people values('10010018','Dark',180,82,'brown','Golden','3842-45ave,Calgary Alberta','m','29-MAY-1989');
INSERT into people values('10010019','Blade',181,82,'brown','Golden','4562-45ave,Calgary Alberta','m','29-MAY-1988');
INSERT into people values('10010020','Princess',167,55,'blue','Golden','7878-78ave,Vancouver BC','f','07-JUL-1988');
INSERT into people values('10010021','Price',188,90,'brown','black','9000-23ave,Toronto OA','m','30-SEP-1982');
INSERT into people values('10010022','Landy',166,52,'blue','brown','9324-67ave,Montreal Que','f','30-SEP-1989');
INSERT into people values('10010023','Mary',165,54,'blue','black','1024-67ave,Montreal Que','f','30-SEP-1984');
INSERT into people values('10010024','Type',174,70,'black','black','2222-101ave,Halifax New','m','30-SEP-1988');
INSERT into people values('10010025','Titan',180,80,'black','black','3333-100ave,Halifax New','m','30-SEP-1993');
INSERT into people values('10010026','Leslin',171,60,'black','black','2233-97ave,Hamilton OA','f','30-SEP-1991');
INSERT into people values('10010027','Unix',176,68,'black','golden','0802-23ave,Hamilton OA','m','21-SEP-1983');
INSERT into people values('10010028','Linux',172,65,'blue','golden','2332-84ave,Edmonton Alberta','m','21-SEP-1983');

INSERT into drive_licence values('ABC-9090','10010010','A',null,'01-JAN-2005','31-DEC-2013');
INSERT into drive_licence values('BCD-9191','10010011','B',null,'01-JUL-2004','30-JUN-2013');
INSERT into drive_licence values('ABC-9292','10010012','C',null,'01-JAN-2007','31-DEC-2015');
INSERT into drive_licence values('CDE-9393','10010013','B',null,'01-JUN-2008','30-DEC-2016');
INSERT into drive_licence values('ABC-9494','10010014','A',null,'01-JAN-2010','31-DEC-2017');
INSERT into drive_licence values('KOK-1093','10010015','nondriving',null,'01-JAN-2009','31-DEC-2015');
INSERT into drive_licence values('KOK-1094','10010016','nondriving',null,'01-JAN-2008','31-DEC-2014');
INSERT into drive_licence values('OIO-1095','10010017','nondriving',null,'01-JAN-2008','31-DEC-2014');
INSERT into drive_licence values('TCG-1026','10010018','B',null,'01-MAR-2010','31-MAY-2016');
INSERT into drive_licence values('TCG-1027','10010019','B',null,'01-MAR-2010','31-MAY-2016');
INSERT into drive_licence values('TCG-1028','10010020','C',null,'01-MAR-2010','31-MAY-2016');
INSERT into drive_licence values('TCG-1029','10010021','A',null,'01-MAR-2010','31-MAY-2016');
INSERT into drive_licence values('TCG-1030','10010022','B',null,'01-MAR-2009','31-MAY-2015');
INSERT into drive_licence values('ABC-9125','10010023','B',null,'01-MAR-2009','31-MAY-2015');
INSERT into drive_licence values('ABC-9126','10010024','nondriving',null,'01-MAR-2009','31-MAY-2015');
INSERT into drive_licence values('ABC-9127','10010025','nondriving',null,'01-MAR-2008','31-MAY-2014');
INSERT into drive_licence values('ABC-9128','10010026','nondriving',null,'01-MAR-2008','31-MAY-2014');
INSERT into drive_licence values('ABC-9129','10010027','B',null,'01-MAR-2008','31-MAY-2014');
INSERT into drive_licence values('ABC-9130','10010028','C',null,'01-MAR-2008','31-MAY-2014');

INSERT into driving_condition values(123123,'Good');
INSERT into driving_condition values(123124,'Poor');
INSERT into driving_condition values(123125,'Exellent');
INSERT into driving_condition values(123126,'Good');
INSERT into driving_condition values(123128,'Poor');
INSERT into driving_condition values(123129,'Excellent');
INSERT into driving_condition values(123130,'Good');
INSERT into driving_condition values(123131,'Poor');
INSERT into driving_condition values(123132,'Excellent');
INSERT into driving_condition values(123133,'Good');
INSERT into driving_condition values(123134,'Poor');
INSERT into driving_condition values(123135,'Excellent');
INSERT into driving_condition values(123136,'Good');
INSERT into driving_condition values(123137,'Poor');
INSERT into driving_condition values(123138,'Excellent');
INSERT into driving_condition values(123139,'Good');
INSERT into driving_condition values(123140,'Poor');
INSERT into driving_condition values(123141,'Good');
INSERT into driving_condition values(123142,'Excellent');

INSERT into restriction values('ABC-9090',123123);
INSERT into restriction values('BCD-9191',123124);
INSERT into restriction values('ABC-9292',123125);
INSERT into restriction values('CDE-9393',123126);
INSERT into restriction values('ABC-9494',123128);
INSERT into restriction values('KOK-1093',123129);
INSERT into restriction values('KOK-1094',123130);
INSERT into restriction values('OIO-1095',123131);
INSERT into restriction values('TCG-1026',123132);
INSERT into restriction values('TCG-1027',123133);
INSERT into restriction values('TCG-1028',123134);
INSERT into restriction values('TCG-1029',123135);
INSERT into restriction values('TCG-1030',123136);
INSERT into restriction values('ABC-9125',123137);
INSERT into restriction values('ABC-9126',123138);
INSERT into restriction values('ABC-9127',123139);
INSERT into restriction values('ABC-9128',123140);
INSERT into restriction values('ABC-9129',123141);
INSERT into restriction values('ABC-9130',123142);

INSERT into vehicle_type values(1,'BUS');
INSERT into vehicle_type values(2,'Semi-truck');
INSERT into vehicle_type values(3,'SUV');
INSERT into vehicle_type values(4,'Sedan');
INSERT into vehicle_type values(5,'Little');

INSERT into vehicle values('AB-29020','Fort','AZO',2004,'red',3);
INSERT into vehicle values('LA-34891','Toyota','Coralla',2002,'black',3);
INSERT into vehicle values('SA-23420','Honda','Achord',2006,'blue',3);
INSERT into vehicle values('AB-45430','BMW','740Li',2007,'blue',4);
INSERT into vehicle values('AB-23450','Benz','GL550',2009,'black',3);
INSERT into vehicle values('AB-90487','Benz','ML350',2010,'black',3);
INSERT into vehicle values('BC-24567','Toyota','Pardo',2008,'red',3);
INSERT into vehicle values('CD-43893','Hydai','PH11',2007,'black',4);
INSERT into vehicle values('CD-23849','Smart','PO09',2010,'white',5);
INSERT into vehicle values('CD-23850','Smart','PO09',2010,'white',5);
INSERT into vehicle values('AB-25234','Benz','GL550',2009,'black',3);
INSERT into vehicle values('LA-34892','Toyota','Coralla',2009,'black',3);
INSERT into vehicle values('AB-29021','Fort','AZO',2008,'red',3);
INSERT into vehicle values('AB-45431','BMW','740Li',2007,'blue',4);
INSERT into vehicle values('AB-92487','Benz','ML350',2010,'black',3);
INSERT into vehicle values('AB-93287','Benz','ML350',2010,'black',3);
INSERT into vehicle values('AB-93282','Toyota','LL21',2009,'black',3);
INSERT into vehicle values('AB-93283','GMC','LL213',2011,'silver',2);
INSERT into vehicle values('AB-93284','GMC','LL213',2011,'silver',2);


INSERT into owner values('10010010','AB-29020','y');
INSERT into owner values('10010011','LA-34891','n');
INSERT into owner values('10010012','SA-23420','y');
INSERT into owner values('10010013','AB-45430','n');
INSERT into owner values('10010014','AB-23450','y');
INSERT into owner values('10010010','AB-90487','y');
INSERT into owner values('10010010','BC-24567','y');
INSERT into owner values('10010015','CD-43893','y');
INSERT into owner values('10010016','CD-23850','y');
INSERT into owner values('10010017','AB-25234','y');
INSERT into owner values('10010018','LA-34892','y');
INSERT into owner values('10010019','AB-29021','y');
INSERT into owner values('10010020','CD-23849','y');
INSERT into owner values('10010021','AB-45431','n');
INSERT into owner values('10010022','AB-92487','y');
INSERT into owner values('10010023','AB-93287','n');
INSERT into owner values('10010024','AB-93282','y');
INSERT into owner values('10010025','AB-93283','y');
INSERT into owner values('10010026','AB-93284','y');
INSERT into owner values('10010024','LA-34891','y');
INSERT into owner values('10010016','AB-45430','y');
INSERT into owner values('10010018','AB-45431','y');
INSERT into owner values('10010018','AB-93287','y');



INSERT into auto_sale values(1203901,'10010015','10010010','AB-29020', '04-DEC-2004',18991);
INSERT into auto_sale values(1203902,'10010016','10010017','LA-34891', '04-MAY-2002',12991);
INSERT into auto_sale values(1203903,'10010016','10010012','SA-23420', '05-JAN-2006',10991);
INSERT into auto_sale values(1203904,'10010016','10010018','AB-45430', '07-JUL-2007',38991);
INSERT into auto_sale values(1203905,'10010017','10010014','AB-23450', '18-MAR-2009',48991);
INSERT into auto_sale values(1203906,'10010017','10010010','AB-90487', '18-MAR-2010',38991);
INSERT into auto_sale values(1203907,'10010017','10010010','BC-24567', '18-MAR-2007',28991);
INSERT into auto_sale values(1203908,'10010018','10010015','CD-43893', '23-OCT-2007',12930);
INSERT into auto_sale values(1203909,'10010016','10010020','CD-23849', '25-OCT-2009',10089);
INSERT into auto_sale values(1203910,'10010016','10010017','AB-25234', '04-MAY-2008',48991);
INSERT into auto_sale values(1203911,'10010016','10010018','LA-34892', '04-MAY-2009',12991);
INSERT into auto_sale values(1203912,'10010018','10010016','CD-23850', '29-MAY-2008',10089);
INSERT into auto_sale values(1203913,'10010018','10010019','AB-25234', '31-MAY-2009',48991);
INSERT into auto_sale values(1203914,'10010018','10010021','AB-45431', '31-MAY-2009',38991);
INSERT into auto_sale values(1203915,'10010018','10010022','AB-92487', '31-MAY-2010',38991);
INSERT into auto_sale values(1203916,'10010018','10010023','AB-93287', '31-MAY-2010',38991);
INSERT into auto_sale values(1203917,'10010018','10010024','AB-93282', '31-MAY-2010',28991);
INSERT into auto_sale values(1203918,'10010018','10010025','AB-93283', '30-SEP-2010',18991);
INSERT into auto_sale values(1203919,'10010018','10010026','AB-93284', '30-SEP-2010',18991);
INSERT into auto_sale values(1203920,'10010018','10010019','AB-29021', '30-OCT-2010',18991);



INSERT into ticket_type values('Parking',50.00);
INSERT into ticket_type values('Accrossing',500.00);
INSERT into ticket_type values('Hiting',700.00);
INSERT into ticket_type values('Speeding',200.00);
INSERT into ticket_type values('Oppositing',800.00);

INSERT into ticket values(1231248,'10010010','AB-29020','10010019','Parking','18-MAR-2009','2349-90Ave, Cal','Parking in the wrong place');
INSERT into ticket values(1231249,'10010011','LA-34891','10010020','Accrossing','18-MAY-2013','4588-111Ave, Edm','Drivng while red lights on');
INSERT into ticket values(1231250,'10010012','SA-23420','10010021','Hiting','12-SEP-2008','2389-101Ave, Edm','Hit a car in the parking area');
INSERT into ticket values(1231251,'10010013','AB-45430','10010022','Speeding','13-SEP-2013','9023-18Ave, Van','Faster than limit');
INSERT into ticket values(1231252,'10010014','AB-23450','10010023','Oppositing','05-OCT-2013','3427-33Ave, Tor','Driving in oppsite direction');
INSERT into ticket values(1231253,'10010024','CD-23849','10010021','Parking','04-SEP-2012','4592-122Ave, Tor','Parking in the wrong place');
INSERT into ticket values(1231254,'10010010','AB-29020','10010022','Speeding','04-SEP-2012','1231-122Ave, Tor','Over speed limit');
INSERT into ticket values(1231255,'10010010','AB-29020','10010022','Speeding','21-SEP-2012','1231-100Ave, Edm','Over speed limit');
INSERT into ticket values(1231256,'10010011','LA-34891','10010022','Parking','30-SEP-2013','1231-100Ave, Edm','Parking in the wrong place');
INSERT into ticket values(1231257,'10010018','LA-34892','10010022','Speeding','21-SEP-2013','1231-100Ave, Edm','Over speed limit');
INSERT into ticket values(1231258,'10010018','LA-34892','10010022','Speeding','21-SEP-2013','1331-100Ave, Edm','Over speed limit');
INSERT into ticket values(1231259,'10010018','LA-34892','10010022','Speeding','21-SEP-2013','1331-100Ave, Edm','Over speed limit');
INSERT into ticket values(1231260,'10010011','LA-34891','10010022','Speeding','21-SEP-2013','1331-100Ave, Edm','Over speed limit');
INSERT into ticket values(1231261,'10010011','LA-34891','10010022','Speeding','21-SEP-2013','1331-100Ave, Edm','Over speed limit');





