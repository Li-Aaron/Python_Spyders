-- sqlite3 test.db 
/*
 * <table> person
 * <column> id name age
 * <value>
 * <condition>
 */

/* common */
CREATE TABLE person (id integer primary key, 
	name varchar(20),
	age integer);
INSERT INTO person(name, age) VALUES ('Ruby',27);
INSERT INTO person(name, age) VALUES ('Sapphire',27);

SELECT * FROM person;
SELECT id FROM person;
SELECT id,name FROM person;
SELECT id,name FROM person WHERE id < 2;
SELECT id,name FROM person WHERE id BETWEEN 1 AND 2;
SELECT id,name FROM person WHERE id = 2;
SELECT id,name FROM person WHERE id = '2';
SELECT id,name FROM person ORDER BY name;
SELECT id,name FROM person ORDER BY age;
UPDATE person SET age = '28' WHERE name = 'Ruby';

INSERT INTO person(name, age) VALUES ('Sapphire2',27);
DELETE FROM person WHERE name = 'Sapphire2';

/* sqlite3 */
.schema person		-- return create table order
.tables				-- return all tables
.indices person		-- return table indexs

-- backup as sql
.output test.sql
.dump
.output stdout

-- backup as csv
.output test.csv
.separator ,
SELECT * FROM person;
.output stdout
.separator |

-- load csv
CREATE TABLE person2 (id integer primary key, 
	name varchar(20)
	age integer);
.import test.csv person2
DROP TABLE person2

/* 事务操作 */
SELECT * FROM person;
BEGIN TRANSACTION;
INSERT INTO person(name,age) VALUES('mother',40);
END; -- 不可ROLLBACK
SELECT * FROM person;

BEGIN TRANSACTION;
INSERT INTO person(name,age) VALUES('mother',40);
SELECT * FROM person;
COMMIT; -- 不可ROLLBACK
SELECT * FROM person;


BEGIN;
INSERT INTO person(name,age) VALUES('mother',40);
SELECT * FROM person;
ROLLBACK;
SELECT * FROM person;





