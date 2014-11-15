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
