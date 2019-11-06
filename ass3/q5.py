# COMP3311 19T3 Assignment 3

import cs3311
import sys
conn = cs3311.connect()

cur = conn.cursor()

if len(sys.argv) == 1:
    arg = 'COMP1521'
else:
    arg = sys.argv[1]

value_list = []
value_list.append(arg)

query = "select * from q5 where code = %s"
cur.execute(query, value_list)
res = cur.fetchall()

res = sorted(res, key=lambda x: (x[2], x[1], x[4]/x[3]))


for each in res:
    percent = (each[4]/each[3])*100 + 0.5
    percent = int(percent)
    print(each[2] + " " + each[1] + " is " + str(percent) + "%" + " full")

cur.close()
conn.close()
