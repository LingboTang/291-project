(select p.sin, p.name, p.addr
 from people p, ticket t
 where t.vdate between TO_DATE ('2013/02/01', 'yyyy/mm/dd')
    AND TO_DATE ('2014/2/01', 'yyyy/mm/dd')
    and p.sin = t.violator_no
    and t.vtype <> 'parking'
    GROUP BY p.sin,p.name, p.addr
    having 3 <= All(select count(*)
                    from people p1, ticket t1
                    where p1.sin = t1.violator_no
                    and p.sin =  p1.sin   
                    GROUP BY t1.violator_no));  





