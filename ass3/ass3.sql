-- COMP3311 19T3 Assignment 3
-- Helper views and functions (if needed)

-- helper views for q1
create or replace view q1_course_count as
select course_id, count(*) from course_enrolments group by course_id;
create or replace view q1 as
select s.code, cc.count, c.quota from q1_course_count as cc, courses as c, subjects as s, terms as t 
where c.id = cc.course_id and c.subject_id = s.id and cc.count > c.quota and c.term_id = t.id
and t.name='19T3' and c.quota > 50;


-- helper views for q2
create or replace view q2_num as select substring(code, 5, 4) as num, substring(code, 1, 4) as str from subjects;
create or replace view q2 as select num, count(*), string_agg(str, ' ' order by str) from q2_num group by num;