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






