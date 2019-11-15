# COMP3311 19T3 Assignment 3

import cs3311
import sys

# -------------Helper Function
def calculate_total_hours(days, timetable):
    total = 0
    for d in days:
        total += 2
        start = 10000
        end = 0
        for t in timetable:
            if t[3] == d and t[4] < start:
                start = t[4]
            if t[3] == d and t[5] > end:
                end = t[5]
        end = (end//100)*60 + end%100
        start = (start//100)*60 + start%100
        total += (end-start)/60.0
    return total

def checkAvail(course, timetable):
    for c in timetable:
        if course[3] != c[3]:
            continue
        elif course[4] >= c[5]:
            continue
        elif course[5] <= c[4]:
            continue
        else:
            return False
    return True

def removeClass(id, timetable):
    for t in timetable:
        if t[1] == id:
            timetable.remove(t)

def checkFinish(course_types, timetable):
    #print(course_types)
    #print(timetable)
    for course in course_types:
        for ct in course_types[course]:
            # find course with type ct in timetable if not found return false
            check = False
            for t in timetable:
                if t[0] == course and t[2] == ct:
                    check = True
                    break
            if check == False:
                return False
            # if find course with type ct, continue
    return True


# ------------------------------Initianization

conn = cs3311.connect()

cur = conn.cursor()
timetable = []
find = False
def dfs(v, visited, graph, types):
    global find
    global timetable
    if find == True:
        return
    visited[v] = True
    # get data
    q = 'select * from q8 where id = %s'
    cur.execute(q, [v])
    res = cur.fetchall()
    for r in res:
        if checkAvail(r, timetable) == True:
            timetable.append(r)
        else:
            removeClass(v, timetable)
            return
    # if it is the last point
    if graph[v] == [] and checkFinish(types, timetable):
        find = True
    # if it is an intermadiate point
    for each in graph[v]:
        if visited[each] == False:
            dfs(each, visited, graph, types)



# ------------------------------Main function
# get arguments from bash
args = []
if (len(sys.argv) == 1):
    args.append('COMP1511')
    args.append('MATH1131')
else:
    args_len = len(sys.argv) - 1
    for i in range(args_len):
        args.append(sys.argv[i+1])

types = {}
course_types = {}
total_hours = 0.0
# find all classes for each type of each course
for course in args:
    value_list = []
    value_list.append(course)
    query = 'select * from q8 where code = %s'
    cur.execute(query, value_list)
    res = cur.fetchall()
    # get all types of meetings
    meeting_types = []
    for r in res:
        meeting_types.append(r[2])
    meeting_types = set(meeting_types)
    meeting_types = list(meeting_types)
    #print(meeting_types)
    # for each class type, find classes
    types[course] = meeting_types
    # store type and course code into t_dic
    t_dic = {}
    for t in meeting_types:
        # find course, type from database
        q = 'select distinct id from q8 where code = %s and name = %s'
        q_list = []
        q_list.append(course)
        q_list.append(t)

        # insert class code into list
        cur.execute(q, q_list)
        cl = cur.fetchall()
        diff_class_code = []
        for c in cl:
            diff_class_code.append(c[0])
        t_dic[t] = diff_class_code
    # update course type: {course: {type : code}}
    course_types[course] = t_dic

#############################################
# put all possible permutations into list
courses = []
for course in course_types:
    #print(course)
    c_typs = course_types[course]
    for c in c_typs:
        course_code = c_typs[c]
        courses.append(course_code)
        #print(course_code)

courses = sorted(courses, key=lambda x: len(x))
# create tree map for courses
course_map = {}
map_count = {}
cnt = 0
for i in range(0, len(courses)-1):
    for each in courses[i]:
        course_map[each] = courses[i+1]
        map_count[each] = cnt
        cnt += 1
for each in courses[-1]:
    course_map[each] = []
    map_count[each] = cnt
    cnt += 1
# sort course_map
course_map = sorted(course_map.items(), key = lambda kv: map_count[kv[0]])
course_map = dict(course_map)


# use dfs to find permutations
# init all visited as -1
visited = {}
for each in course_map:
    visited[each] = False

dfs(list(course_map.keys())[0], visited, course_map, types)


# print timetable
day_dic = {"Mon" : 1, "Tue" : 2, "Wed" : 3, "Thu" : 4, "Fri" : 5}

# get all days and sort 
days = []
for time in timetable:
    days.append(time[3])
days = set(days)
days = list(days)
days = sorted(days, key= lambda x: day_dic[x])

# calculate total hours
total_hours = calculate_total_hours(days, timetable)

print("Total hours: {:.1f}".format(total_hours))
for d in days:
    # find meetings on this day
    print("  {}".format(d))
    meeting_day = []
    for cls in timetable:
        if cls[3] == d:
            meeting_day.append(cls)
    meeting_day = sorted(meeting_day, key= lambda x: x[4])
    # print courses in that day
    for each in meeting_day:
        print("    {} {}: {}-{}".format(each[0], each[2], each[4], each[5]))


cur.close()
conn.close()
