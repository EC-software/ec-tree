-- collision_short source

CREATE VIEW collision_short as
  select count(*), shorthash
  from files
  group by shorthash
  order by count(*) desc
;


select *
  from files
  where shorthash = "290d8b7082318d5a04766ea45c89e796ccf217e7"
;