prompt Question 1 - lingbo

select serial_no
from vehicle,owner,people
where serial_no = owner.vehicle_id
       and owner.owner_id = people.sin
       and addr not like '%Edmonton%';
prompt Question 2 - lingbo

select distinct name, addr
from people, owner A,owner B, owner C, vehicle D,vehicle E,vehicle F,vehicle_type
where A.owner_id = sin
and B.owner_id = sin
and C.owner_id = sin
and A.vehicle_id = D.serial_no
and B.vehicle_id = E.serial_no
and C.vehicle_id = F.serial_no
and D.type_id = vehicle_type.type_id
and E.type_id = vehicle_type.type_id
and F.type_id = vehicle_type.type_id
and D.serial_no <> E.serial_no
and E.serial_no <> F.serial_no
and D.serial_no <> F.serial_no
and vehicle_type.type_id >= 3;

prompt Question 3 - lingbo

select distinct licence_no,name
from people,drive_licence,owner,vehicle
where people.sin = owner.owner_id
and owner.vehicle_id = serial_no
and owner.owner_id = drive_licence.sin
and drive_licence.class <> 'nondriving'
minus
select distinct licence_no, name
from drive_licence, vehicle, people, owner
where  people.sin = drive_licence.sin
and owner.vehicle_id = vehicle.serial_no
and owner.owner_id = people.sin
and vehicle.color = 'red';
prompt Question 4 - lingbo

select distinct people.name
from people, ticket,ticket_type,drive_licence
where people.sin=ticket.violator_no
and ticket.vtype = ticket_type.vtype
and people.sin = drive_licence.sin
and drive_licence.class <> 'nondriving'
group by people.name
having SUM(ticket_type.fine) >= all (select SUM(ticket_type.fine)/count(distinct drive_licence.sin)
	       From ticket,ticket_type,drive_licence,people
	       where ticket.vtype = ticket_type.vtype
	       and drive_licence.sin = ticket.violator_no
	       and drive_licence.class <> 'nondriving'
	       group by people.name);


prompt Question 5 - lingbo

Select AVG(auto_sale.price),
       vehicle_type.type,
       extract(year 
       from auto_sale.s_date) as year
from auto_sale,vehicle,vehicle_type
where auto_sale.vehicle_id = vehicle.serial_no
and vehicle.type_id = vehicle_type .type_id
and auto_sale.s_date between to_date ('01-JAN-2003', 'DD-Mon-YYYY') AND to_date('31-DEC-2010', 'DD-Mon-YYYY')
group by extract(year from auto_sale.s_date),vehicle_type.type;


prompt Question 6 - lingbo

select name
from   people
minus
select name
from   people, owner, vehicle A
where  owner.vehicle_id = A.serial_no 
and people.sin = owner.owner_id 
and (A.maker, A.model, A.year) in (select  B.maker, B.model, B.year
           			   from    vehicle B
           			   group by B.maker, B.model, B.year 
           			   having  count(*)>= all(select  count(*)
                                                             from    vehicle C
                                                             where   B.year = C.year
                                                             group by C.maker,C.model,C.year
                                                            )
                                  );
prompt Question 7 - lingbo

select people.sin,people.name,people.addr
from people,ticket
where people.sin = ticket.violator_no
and ticket.vtype <> 'Parking'
and ticket.vdate >= (sysdate -365)
group by people.sin,people.name,people.addr
having  3 = all(select count(*) from people B, ticket C
	   	where B.sin = people.sin
	   	and B.sin = C.violator_no
		and C.vtype <> 'Parking' 
	   	group by C.violator_no);
prompt Question 8 - lingbo

create view vehicle_history (serial_no, no_sales, average_price, total_tickets) as
select  vehicle.serial_no, count(distinct seller_id), AVG(price), count(distinct ticket.ticket_no)
from       vehicle, auto_sale, ticket
where ticket.vehicle_id (+) = vehicle.serial_no
and auto_sale.vehicle_id = vehicle.serial_no
group by vehicle.serial_no;
prompt Question 9 - lingbo

select name
from   people, owner, vehicle_history
where  owner.vehicle_id = vehicle_history.serial_no 
and    people.sin = owner.owner_id    
and    ( (vehicle_history.total_tickets >= all(select total_tickets from vehicle_history))
         or
         (vehicle_history.no_sales  >= all(select no_sales from vehicle_history))
	 or
         (vehicle_history.average_price <= all(select average_price from vehicle_history))
       );






