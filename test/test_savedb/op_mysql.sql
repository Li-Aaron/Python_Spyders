-- mysql -u root -p
-- mysql -u root -p < [WORKING_DIR]\op_mysql.sql
-- source [WORKING_DIR]\op_mysql.sql
-- \. [WORKING_DIR]\op_mysql.sql
CREATE DATABASE test CHARACTER SET gbk;
USE test;

CREATE TABLE student
(
	id int unsigned not null auto_increment primary key,
	name char(8) not null,
	sex char(4) not null,
	age tinyint unsigned not null
);

INSERT INTO student values (NULL, "红宝石", "男", 24);
INSERT INTO student(name,sex,age) values ("蓝宝石", "女", 22);
INSERT INTO student(name,sex,age) values ("蓝宝石", "女", 22);
UPDATE student SET age = 18 WHERE name = "蓝宝石";
SELECT name,age FROM student LIMIT 1000;
DELETE FROM student WHERE id > 2;

ALTER TABLE student ADD address VARCHAR(60) AFTER age;
ALTER TABLE student CHANGE address addr CHAR(60);
ALTER TABLE student DROP addr;
ALTER TABLE student RENAME students;

DROP TABLE students;

/* MySQL Commands */
show databases;
GRANT SELECT,INSERT,UPDATE,DELETE on test.* to ruby@localhost IDENTIFIED BY '123';
-- mysql -h 127.0.0.1 -u ruby -p
-- mysqldump -u root -p test > test.sql
-- mysqldump -u root -p test student > test.sql