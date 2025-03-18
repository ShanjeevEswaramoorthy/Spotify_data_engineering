import mysql.connector
from mysql.connector import Error

try:

    # connecting your python code to mysql database
    connector = mysql.connector.connect(
        host='localhost',
        database='shanjeev',
        user='root',
        password='Shanjeev_root'
    )

    if connector.is_connected():
        print('mysql connected')

        # cursor which is used to excute the query and
        cursor = connector.cursor()

        # query = 'insert into python_jdbc values('shanjeev'),('kumar')'
        query = "select * from python_jdbc"

        cursor.execute(query)

        # fetch all the records from database
        fetchRecords = cursor.fetchall()

        for record in fetchRecords:
            print(record)

        cursor.close()
        connector.close()

except Error as e:
    print('error occur while fetching ->', e)

finally:
    #  close the connecting once all query done
    if connector.is_connected():
        cursor.close()
        connector.close()

        #  ---> insert query method for jdbc
        # query = "INSERT INTO python_jdbc (name) VALUES (%s), (%s)"
        # values = [("shanjeev", "kumar")]
        #
        # cursor.executemany(query,values)
        #
        # # commit which is used to merge the changes in mysql database
        # connector.commit()
