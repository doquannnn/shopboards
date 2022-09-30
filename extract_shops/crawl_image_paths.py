import cx_Oracle
import os
from datetime import datetime


def crawl_paths(start: datetime, end: datetime, dir: str = "timestamps") -> str:
    CONN_INFO = {
        "host": "10.30.174.177",
        "port": 8645,
        "user": "NUTIFOOD",
        "psw": "IcT@NuT1F00d#2016",
        "service": "nuti",
    }
    # dsn_tns = cx_Oracle.makedsn("10.30.174.177", 8645, "nuti")

    # conn = cx_Oracle.connect(user='NUTIFOOD', password='IcT@NuT1F00d#2016', dsn=dsn_tns)
    CONN_STR = "{user}/{psw}@{host}:{port}/{service}".format(**CONN_INFO)

    try:
        con = cx_Oracle.connect(CONN_STR)
        # con = cx_Oracle.connect(user="NUTIFOOD", password="IcT@NuT1F00d#2016", dsn=dsn_tns)
    except cx_Oracle.DatabaseError as er:
        print("There is an error in the Oracle database:", er)
    else:
        try:
            cur = con.cursor()
            s, e = start, end
            start_range = (datetime.now() - s).days
            end_range = (datetime.now() - e).days

            sqlquery = f"""SELECT Customer.SHORT_CODE, MEDIA_ITEM.URL,
            MEDIA_ITEM.create_date, Object_type
            FROM Customer
            INNER JOIN MEDIA_ITEM ON Customer.Customer_ID=MEDIA_ITEM.OBJECT_ID
            WHERE MEDIA_ITEM.create_date >= trunc(sysdate - {start_range})
            and MEDIA_ITEM.create_date <= trunc(sysdate - {end_range}) and MEDIA_ITEM.Object_type=2"""

            cur.execute(sqlquery)
            res = cur.fetchall()
            filename = f"{start.day}_{start.month}_{start.year}-{end.day}_{end.month}_{end.year}"
            os.chdir(os.path.join(os.getcwd(), dir))

            with open(f"{filename}.txt", "w") as wf:
                for row in res:
                    wf.write(str(row) + "\n")

        except cx_Oracle.DatabaseError as er:
            print("There is an error in the Oracle database:", er)

        except Exception as er:
            print("Error:" + str(er))

        finally:
            if cur:
                cur.close()
                con.close()
    return "Table process successful"


if __name__ == "__main__":
    start = datetime(2022, 7, 18)
    end = datetime(2022, 8, 18)
    print(crawl_paths(start, end))
