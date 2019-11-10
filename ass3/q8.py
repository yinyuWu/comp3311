# COMP3311 19T3 Assignment 3

import cs3311
import sys

def deleteMeetings(id, timetable):
    for t in timetable:
        if t[1] == id:
            timetable.remove(t)


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

def meeting_check(to_add, timetable):
    for t in timetable:
        # to_add is not the same day, before t, after t allowed
        if to_add[3] != t[3]:
            continue
        if to_add[3] == t[3] and to_add[5] <= t[4]:
            continue
        if to_add[3] == t[3] and to_add[4] >= t[5]:
            continue
        else:
            return False
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
    class_list = []
    for t in meeting_types:
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
            success_cnt = 0
            # insert meetings to class table
            for each in res:
                if (meeting_check(each, timetable) == False):
                    # if fail to insert, delete all classes inserted
                    deleteMeetings(dc, timetable)
                    break
                timetable.append(each)
                success_cnt += 1
            # if all meetings are inserted successfully
            if (success_cnt == len(res)):
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
