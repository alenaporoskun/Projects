chcp 1251
set NLS_LANG = AMERICAN_AMERICA.CL8MSWIN1251

ECHO SET LINESIZE 200 > startup.sql
ECHO SET PAGESIZE 40 >> startup.sql
ECHO SET NULL (null) >> startup.sql

client\sqlplus.exe student_pm81_08/student@195.182.202.156:15215/XEPDB1 @startup