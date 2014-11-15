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


