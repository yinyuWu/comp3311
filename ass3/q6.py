# COMP3311 19T3 Assignment 3

import cs3311

conn = cs3311.connect()
cur = conn.cursor()

query = "select id, weeks, weeks_binary from meetings"
cur.execute(query)
res = cur.fetchall()
# split '1-5,7-11'
for r in res:
    wb = '00000000000'
    wb = list(wb)
    weeks = r[1]
    # if contains 'N' or '<'
    if weeks.find('N') >= 0 or weeks.find('<') >= 0:
        wb = ''.join(wb)
        q = 'update meetings set weeks_binary = ' + wb + ' where id = ' + str(r[0])
        cur.execute(q)
        continue
    #split by ','
    weeks = weeks.split(',')
    for w in weeks:
        # we have 1-5
        start_end = w.split('-')
        # be ['1', '5'] and convert to int or ['2']
        start_end = [int(i) for i in start_end]
        # modify weeks_binary acoording to start end
        # if ['2']
        if len(start_end) == 1:
            j = start_end[0]
            wb[j-1] = '1'
        # otherwise
        else:
            for j in range(start_end[0], start_end[1]+1):
                wb[j-1] = '1'
    wb = ''.join(wb)
    # update
    q = 'update meetings set weeks_binary = ' + wb + ' where id = ' + str(r[0])
    cur.execute(q)
conn.commit()
cur.close()
conn.close()
