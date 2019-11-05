# COMP3311 19T3 Assignment 3

import cs3311
import sys
conn = cs3311.connect()

cur = conn.cursor()

value_list = []
value_list.append(int(sys.argv[1]))
query = "select * from q2 where count = %s"

cur.execute(query, value_list)

res = cur.fetchall()
for each in res:
    print("{}: {}".format(each[0], each[2]))


cur.close()
conn.close()
