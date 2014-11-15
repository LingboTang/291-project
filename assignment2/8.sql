prompt Question 8 - lingbo

create view vehicle_history (serial_no, no_sales, average_price, total_tickets) as
select  vehicle.serial_no, count(distinct seller_id), AVG(price), count(distinct ticket.ticket_no)
from       vehicle, auto_sale, ticket
where ticket.vehicle_id (+) = vehicle.serial_no
and auto_sale.vehicle_id = vehicle.serial_no
group by vehicle.serial_no;
