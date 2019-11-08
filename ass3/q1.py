# COMP3311 19T3 Assignment 3

import cs3311
conn = cs3311.connect()

cur = conn.cursor()
query = "select * from q1 order by code"
cur.execute(query)
res = cur.fetchall()
for each in res:
    percent = (each[1]/each[2]) * 100
    percent = int(round(percent, 0))
    print("{} {}%".format(each[0], str(percent)))




cur.close()
conn.close()
