select distinct ticket_no
from ticket,ticket_type
where ticket.vtype = ticket_type.vtype
and ticket_type.fine > all (select SUM(ticket_type.fine)/count(ticket.ticket_no)
		            from ticket,ticket_type
			    group by ticket_type.fine, ticket.ticket_no);


select distinct name
from people, ticket,ticket_type
where people.sin=ticket.violator_no
and ticket.vtype = ticket_type.vtype
and ticket_type.fine > all(select SUM(ticket_type.fine)/count(ticket.ticket_no)
	       From ticket,ticket_type,drive_licence
	       where ticket.vtype = ticket_type.vtype
	       and drive_licence.sin = ticket.violator_no
	       and people.sin = drive_licence.sin
	       group by ticket.ticket_no,ticket_type.fine)
minus
select distinct name
from ticket, drive_licence, people
where people.sin = ticket.violator_no
and ticket.violator_no not in (select drive_licence.sin
			 from drive_licence);

