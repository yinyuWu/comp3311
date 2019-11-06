# COMP3311 19T3 Assignment 3

import cs3311
import sys
import time

start = time.time()
conn = cs3311.connect()

cur = conn.cursor()

if len(sys.argv) == 1:
    arg = 'ENGG'
else:
    arg = sys.argv[1]

value_list = []
value_list.append(arg)

query = "select * from q3 where str = %s"

cur.execute(query, value_list)
res = cur.fetchall()

building_list = []

for each in res:
    building_list.append(each[0])

building_list = (set)(building_list)
building_list = (list)(building_list)
building_list.sort()

for each in building_list:
    print(each)
    # find corresponding courses
    course_list = []
    for r in res:
        if (r[0] == each):
            course_list.append(r[1])
    course = (set)(course_list)
    course = (list)(course)
    c = ''
    course.sort(key=lambda x: (int)(c.join(list(x)[4:])))
    # print results
    for each in course:
        print(" " + each)
    
# TODO

cur.close()
conn.close()

