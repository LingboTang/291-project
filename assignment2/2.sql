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

