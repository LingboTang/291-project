(select distinct dl.licence_no, p.name
 from drive_licence dl, vehicle v, people p, owner o
 where (dl.class <> 'nondriving'
    and o.vehicle_id = v.serial_no
    and p.sin = dl.sin
    and o.owner_id = p.sin)
minus
(select distinct dl.licence_no, p.name
 from drive_licence dl, vehicle v, people p, owner o
 where  v.color = 'red'
    and o.vehicle_id = v.serial_no
    and p.sin = dl.sin
    and o.owner_id = p.sin));
