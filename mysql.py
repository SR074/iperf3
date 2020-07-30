'''



stmt = "select * from company where name = %s"
cursor.execute(stmt, ("McDonald's", ))

... # read data

cursor.close()
cnx.close()
'''