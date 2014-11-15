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


