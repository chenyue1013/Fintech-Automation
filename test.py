import psycopg2
import pandas as pd
from sshtunnel import SSHTunnelForwarder

try:
    ssh_host = '54.89.138.43'
    ssh_port = 22
    ssh_username = 'ubuntu'

    db_host = 'fta-prod-db-proxy-read-only.endpoint.proxy-cl2j5mnkf6nl.us-east-1.rds.amazonaws.com'
    db_port = 5432
    db_name = 'ychen'
    db_password = 'zUYwH!QP!nZu'

    server = SSHTunnelForwarder(
        ssh_address_or_host=(ssh_host, ssh_port),
        ssh_username=ssh_username,
        ssh_pkey='C:/Users/86157/Downloads/PGSQL Client 1.pem',
        remote_bind_address=(db_host, db_port)
    )
    server.start()

    conn = psycopg2.connect(
        database='fta_prod',
        user=db_name,
        password=db_password,
        host='127.0.0.1',
        port=server.local_bind_port
    )
    print(conn)

    Creditquery = 'SELECT "Money Movement Record Type", "Transfer type", "ACH Batch", "Sleeve Account", "Account Number", "Amount" FROM actc."Credit Report(Daily)"'
    data2 = pd.read_sql(Creditquery, conn)

    print(data2)

except Exception as e:
    print("An error occurred:", e)

finally:
    if 'conn' in locals():
        conn.close()
    if 'server' in locals():
        server.stop()
