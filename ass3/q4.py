# COMP3311 19T3 Assignment 3

import cs3311
import sys
conn = cs3311.connect()

cur = conn.cursor()

if len(sys.argv) == 1:
    arg = 'ENGG'
else:
    arg = sys.argv[1]

value_list = []
value_list.append(arg)

query = "select * from q4 where str = %s"
cur.execute(query, value_list)
res = cur.fetchall()

# get terms
terms = []
for each in res:
    terms.append(each[1])
terms = set(terms)
terms = list(terms)
terms.sort()

# print courses and count for each term
for each in terms:
    print(each)
    # find corresponding courses
    courses = []
    for r in res:
        if r[1] == each:
            courses.append((r[0], r[3]))
    courses.sort(key=lambda x: x[0])
    for c in courses:
        print(" " + c[0] + "(" + str(c[1]) + ")")

cur.close()
conn.close()
