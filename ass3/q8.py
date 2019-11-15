# COMP3311 19T3 Assignment 3

import cs3311
import sys

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
        if course[4] >= c[5]:
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




conn = cs3311.connect()

cur = conn.cursor()

# get arguments from bash
args = []
if (len(sys.argv) == 1):
    args.append('COMP1511')
    args.append('MATH1131')
else:
    args_len = len(sys.argv) - 1
    for i in range(args_len):
        args.append(sys.argv[i+1])

timetable = []
course_types = {}
total_hours = 0.0
# for each course find a timetable
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
    course_types[course] = meeting_types

while (1):
    if checkFinish(course_types, timetable) == True:
        break

    for course in course_types:
        class_list = []
        for t in course_types[course]:
            q_list = []
            q_list.append(course)
            q_list.append(t)
            q = 'select distinct id from q8 where code = %s and name = %s'
            cur.execute(q, q_list)
            cl = cur.fetchall()
            # insert different classes' code into list
            diff_class = []
            for c in cl:
                diff_class.append(c[0])
            #print(diff_class)
            # insert meetings into timetable
            for dc in diff_class:
                q = 'select * from q8 where id = %s'
                cur.execute(q, [dc])
                res = cur.fetchall()
                # insert meetings with code 'dc' to class table
                # if insert successfully, we don't need other classes then break
                insert_success = True
                for r in res:
                    if checkAvail(r, timetable) == False:
                        removeClass(r[1], timetable)
                        insert_success = False
                        break
                    else:
                        timetable.append(r)
                if (insert_success == True):
                    break
                



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
