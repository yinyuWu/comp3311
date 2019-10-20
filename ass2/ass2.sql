-- COMP3311 19T3 Assignment 2
-- Written by <<insert your name here>>

-- Q1 Which movies are more than 6 hours long? 

create or replace view Q1(title)
as select main_title from Titles where format = 'movie' and runtime > 360;


-- Q2 What different formats are there in Titles, and how many of each?

create or replace view Q2(format, ntitles)
as select format, count(*) from Titles group by format;


-- Q3 What are the top 10 movies that received more than 1000 votes?

create or replace view Q3(title, rating, nvotes)
as select main_title, rating, nvotes from Titles where nvotes>1000 AND format='movie' order by rating DESC limit 10;


-- Q4 What are the top-rating TV series and how many episodes did each have?

create or replace view Q4(title, nepisodes)
as select t.main_title, count(*) from Titles as t, Episodes as e where e.parent_id = t.id AND (t.format = 'tvSeries' or t.format = 'tvMiniSeries') AND t.rating = 10.0 group by t.main_title;


-- Q5 Which movie was released in the most languages?
create or replace view languageCount as select title_id, count(distinct language) from Aliases where title_id in (select id from Titles where format = 'movie') group by title_id;
create or replace view Q5(title, nlanguages)
as select t.main_title, l.count from Titles as t, languageCount as l where t.id = l.title_id AND l.count >= all(select count from languageCount);


-- Q6 Which actor has the highest average rating in movies that they're known for?
create or replace view q6_name_rating as select n.id, n.name, k.title_id, t.rating from Names as n, Titles as t, Known_for as k where k.title_id=t.id AND k.name_id = n.id AND t.format='movie' AND t.rating IS NOT NULL;
create or replace view q6_actor_rating as select * from q6_name_rating where id in (select name_id from Worked_as where work_role = 'actor');
create or replace view q6_actor_avg as select id, name, avg(rating), count(*) from q6_actor_rating group by id, name;
create or replace view Q6(name) as select name from q6_actor_avg where avg = (select max(avg) from q6_actor_avg where count>1);

-- Q7 For each movie with more than 3 genres, show the movie title and a comma-separated list of the genres

create or replace view q7_genres as select t.id, t.main_title, count(*),string_agg(g.genre, ';' order by g.genre) genres from titles as t, title_genres as g where t.id = g.title_id AND t.format = 'movie' group by t.id;
create or replace view Q7(title,genres)
as select main_title, genres from q7_genres where count > 3;

-- Q8 Get the names of all people who had both actor and crew roles on the same movie

create or replace view Q8(name)
as select name from names where id in (select a.name_id from Actor_roles as a, Titles as t where a.title_id = t.id AND t.format='movie' AND a.name_id in (select name_id from Crew_roles where title_id=t.id));

-- Q9 Who was the youngest person to have an acting role in a movie, and how old were they when the movie started?
create or replace view q9_role_title as select n.id, n.name, n.birth_year, a.title_id, t.start_year, start_year - birth_year as age from Names as n, Actor_roles as a, Titles as t where t.id = a.title_id AND n.id = a.name_id AND t.format = 'movie';
create or replace view Q9(name,age)
as select name, age from q9_role_title where age = (select min(age) from q9_role_title);

-- Q10 Write a PLpgSQL function that, given part of a title, shows the full title and the total size of the cast and crew

create or replace function
	Q10(partial_title text) returns setof text
as $$
declare
	r record;
	full_name text := '';
	cnt integer;
begin
	for r in select t.id, t.main_title, count(*) from titles as t, principals as p where p.title_id = t.id AND main_title ILIKE '%' || partial_title || '%' group by  t.id
	loop
		full_name := r.main_title;
		cnt := r.count;
		full_name := full_name || ' has' || to_char(cnt, '9') || E' cast and crew';
		return next full_name;
	end loop;
	if (not found) then
		return next 'No matching titles';
	end if;
end;
$$ language plpgsql;

