prompt Question 6 - lingbo

select name
from   people
minus
select name
from   people, owner, vehicle A
where  owner.vehicle_id = A.serial_no 
and people.sin = owner.owner_id 
and (A.maker, A.model, A.year) in (select  B.maker, B.model, B.year
           			   from    vehicle B
           			   group by B.maker, B.model, B.year 
           			   having  count(*)>= all(select  count(*)
                                                             from    vehicle C
                                                             where   B.year = C.year
                                                             group by C.maker,C.model,C.year
                                                            )
                                  );
