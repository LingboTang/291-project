CREATE VIEW vehicle_history (vehicle_no, number_sales, average_price, total_tickets) AS
    (SELECT distinct v1.serial_no, count(distinct aus.transaction_id), SUM(aus.price)/count(aus.transaction_id), count(distinct t.ticket_no)
    from auto_sale aus, owner o, vehicle v1
    left outer join ticket t on t.vehicle_id = v1.serial_no
     where  aus.vehicle_id = v1.serial_no
     GROUP BY v1.serial_no); 


