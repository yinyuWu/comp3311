# COMP3311 19T3 Assignment 3

import cs3311
import sys
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
    class_list = []
    for t in meeting_types:
        q_list = []
        q_list.append(course)
        q_list.append(t)
        q = 'select distinct id from q8 where code = %s and name = %s'
        cur.execute(q, q_list)
        cl = cur.fetchall()
        # insert different classes into list
        diff_class = []
        for c in cl:
            diff_class.append(c[0])
        #print(diff_class)
        # insert meetings into timetable
        q = 'select * from q8 where id = %s'
        cur.execute(q, [diff_class[0]])
        res = cur.fetchall()
        # insert meetings to class table
        for each in res:
            timetable.append(each)
# print timetable
day = {"Mon" : 1, "Tue" : 2, "Wed" : 3, "Thu" : 4, "Fri" : 5}



cur.close()
conn.close()
