-- RType SQL Boot script
--
.print "> RType 2017 setup..."
create table if not exists rtype(
 key text unique,
value text);

-- delete from rtype;
insert or ignore into rtype values('version',0.1);
insert or ignore into rtype values('product_name','RType');
-- Default FK regexp
insert or ignore into rtype values('fk_regexp','.*_ID');

attach database ":memory:" as fk_validator;

-- Demo table
create table if not exists person(
 person_id integer primary key autoincrement,
 name text,
 surname text
 );

create table if not exists car(
 car_id integer primary key autoincrement,
 owber_person_id integer,
 model text,
 year integer);


-- Select RANK EMULATION
/*
SELECT Products.Product,
DENSE_RANK() OVER (ORDER BY Products.Code DESC) AS Rank
FROM Products;

In SQLite:

SELECT Product,
(SELECT COUNT()+1 FROM (
    SELECT DISTINCT Code FROM Products AS t WHERE Code < Products.Code)
) AS Rank
FROM Products;
*/
.print ">> Demo table ok"

.print ">>> Emitting json configuration"
--json_object('rtype_dump',
-- json_set('{"a":2,"c":4}', '$.c', json_array(97,96)) → '{"a":2,"c":[97,96]}'
select json_set('{"config": "cfg"}','$.config',C.X) from
       (select json_group_object(key,value) AS X from rtype
order by key) C;

select * from rtype;
-- .dump

-- .mode cvs
-- .separator ;
-- .import
