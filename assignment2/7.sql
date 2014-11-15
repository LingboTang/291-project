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
