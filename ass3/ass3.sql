-- COMP3311 19T3 Assignment 3
-- Helper views and functions (if needed)

create or replace view course_count as
select course_id, count(*) from course_enrolments;
create or replace view q1 as
select c.id, s.title, cc.count from course_count as cc, courses as c, subjects as s
where c.id = cc.course_id and 
