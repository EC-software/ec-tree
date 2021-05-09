CREATE VIEW collision_short as 
  select count(*), shorthash 
  from files 
  where shorthash <> ""
  group by shorthash 
  having count(*) > 1
  order by count(*) desc
;