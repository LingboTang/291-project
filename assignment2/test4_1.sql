select name
from   people p, drive_licence d, ticket t, ticket_type tt
where  p.sin = d.sin
       and d.class <> 'nondriving'
       and p.sin = t.violator_no
       and t.vtype = tt.vtype
       group by p.sin, p.name
       having SUM(tt.fine) >= all (select sum(tt.fine)/count(distinct d.sin)
                                   from   drive_licence d,ticket t,ticket_type tt
                                   where  d.class <> 'nondriving'
                                          and t.violator_no = d.sin
                                          and tt.vtype = t.vtype);
