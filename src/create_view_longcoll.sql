CREATE VIEW collision_long as 
  select count(*), longhash 
  from files 
  where longhash <> ""
  group by longhash 
  having count(*) > 1
  order by count(*) desc
;