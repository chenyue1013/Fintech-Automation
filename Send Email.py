import pandas as pd
import psycopg2
from sshtunnel import SSHTunnelForwarder
import datetime
import win32com.client as win32

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

data1 = pd.read_sql(Totalquery, conn)

print('data1')
nowTime = datetime.datetime.now().strftime('%Y-%m-%d')
output_file_path1 = 'C:/Users/86157/Desktop/Email/新建文件夹/ACTC Total Balance Report_'+str(nowTime)+'.csv'

data1.to_csv(output_file_path1, index=False)


outlook = win32.Dispatch('Outlook.Application')
print("Outlook launched successfully!")
mail = outlook.CreateItem(0)
mail.To = 'ychen@fintechautomation.com'
mail.CC = 'ychen@fintechautomation.com'
mail.Subject = 'test1'
mail.Body = '这是一封测试邮件'
mail.Importance = 2
mail.Attachments.Add(output_file_path1)
mail.Send()

print("保存成功")
