import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder
import datetime

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

# Connact Database
Totalquery = 'SELECT "Financial Account", "Financial Account Number", "Sub Account", "Sub Account Number", "Branch Code", "Balance After Transaction Occurs", "Balance" FROM actc."Total Balance Report";'
Creditquery = 'SELECT "Money Movement Record Type", "Transfer type", "ACH Batch", "Sleeve Account", "Account Number", "Amount" FROM actc."Credit Report(Daily)";'
Debitquery = 'SELECT "Money Movement Record Type","Transfer type","ACH Batch","Sleeve Account","Account Number","Amount" FROM actc."Debit Report(Daily)";'
Total21query = 'SELECT "Financial Account", "Financial Account Number", "Sub Account", "Sub Account Number", "Branch Code", "Balance After Transaction Occurs", "Balance" FROM actc."21 Accounts Total Balance Report";'

# Extract data to DataFrame
data1 = pd.read_sql(Totalquery, conn)
data2 = pd.read_sql(Creditquery, conn)
data3 = pd.read_sql(Debitquery, conn)
data21 = pd.read_sql(Total21query, conn)    

print('data1')
nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
print(nowTime)

output_file_path1 = 'C:/Users/86157/Desktop/Email/新建文件夹/ACTC Total Balance Report_'+str(nowTime)+'.csv'
output_file_path2 = 'C:/Users/86157/Desktop/Email/新建文件夹/ACTC Credit Report(Daily)_'+str(nowTime)+'.csv'
output_file_path3 = 'C:/Users/86157/Desktop/Email/新建文件夹/ACTC Debit Report(Daily)_'+str(nowTime)+'.csv'
output_file_path21 = 'C:/Users/86157/Desktop/Email/新建文件夹/ACTC 21 Accounts Total Balance Report_'+str(nowTime)+'.csv'

data1.to_csv(output_file_path1, index=False)
data2.to_csv(output_file_path2, index=False)
data3.to_csv(output_file_path3, index=False)
data21.to_csv(output_file_path21, index=False)

print("保存成功")

# Connact Database
stearnsTotalquery = 'SELECT "Financial Account", "Financial Account Number", "Sub Account", "Sub Account Number", "Branch Code", "Balance After Transaction Occurs", "Balance" FROM stearns_bank."Total Balance Report"'
stearnsCreditquery = 'SELECT "Money Movement Record Type", "Transfer type", "ACH Batch", "Sleeve Account", "Account Number", "Amount" FROM stearns_bank."Credit Report(Daily)"'
stearnsDebitquery = 'SELECT "Money Movement Record Type","Transfer type","ACH Batch","Sleeve Account","Account Number","Amount" FROM stearns_bank."Debit Report(Daily)"'
# Extract data to DataFrame
data4 = pd.read_sql(stearnsTotalquery, conn)
data5 = pd.read_sql(stearnsCreditquery, conn)
data6 = pd.read_sql(stearnsDebitquery, conn)
print('data1')

output_file_path4 = 'C:/Users/86157/Desktop/Email/新建文件夹/Stearns Bank Total Balance Report_'+str(nowTime)+'.csv'
output_file_path5 = 'C:/Users/86157/Desktop/Email/新建文件夹/Stearns Bank Credit Report(Daily)_'+str(nowTime)+'.csv'
output_file_path6 = 'C:/Users/86157/Desktop/Email/新建文件夹/Stearns Bank Debit Report(Daily)_'+str(nowTime)+'.csv'

data4.to_csv(output_file_path4, index=False)
data5.to_csv(output_file_path5, index=False)
data6.to_csv(output_file_path6, index=False)

print("保存成功")
