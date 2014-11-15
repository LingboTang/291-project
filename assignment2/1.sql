prompt Question 1 - lingbo

select serial_no
from vehicle,owner,people
where serial_no = owner.vehicle_id
       and owner.owner_id = people.sin
       and addr not like '%Edmonton%';
