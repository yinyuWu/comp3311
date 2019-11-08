# COMP3311 19T3 Assignment 3

import cs3311
import sys
conn = cs3311.connect()

cur = conn.cursor()

if len(sys.argv) == 1:
    arg = '19T1'
else:
    arg = sys.argv[1]

value_list = []
value_list.append(arg)

# get all rooms
query_total = 'select code from rooms where code like \'K-%\''
cur.execute(query_total)
total = cur.fetchall()
total = len(total)

# get # rooms that use >= 10*20 hours totally
query_cnt = 'select count(*) from q7 where sum >= 10*20 and name = %s'
cur.execute(query_cnt, value_list)
cnt = total - cur.fetchone()[0]
percent = (cnt/total)*100
percent = round(percent, 1)
print(str(percent) + '%')


cur.close()
conn.close()
