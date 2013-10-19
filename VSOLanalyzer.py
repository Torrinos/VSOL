#!/usr/bin/env python2
#coding=utf8
import codecs
import re
import pymysql
import numpy as np
import scipy as sp

#connecting to mysql
database = pymysql.connect(host='localhost', port=8889, user='user', passwd='pass', db='VSOL', charset='utf8')
cursor = database.cursor()

#connecting to file
ofile=codecs.open('VSOL_results',mode='w', encoding='utf-8')

#fetching summary
cursor.execute("""SELECT
SUM( IF( `VS` != 0,1,0 ) ) AS Total_Teams,
SUM( IF( `VS` != 0 AND (`PK`+`KM`+`D` != 0 OR `PD`+`SK`+`G` != 0) ,1,0)) AS Non_Empty_Teams,
SUM( IF( `VS` !=0 AND (`PK`+`KM`+`D` > `PD`+`SK`+`G`),1,0)) AS Sun_Teams,
SUM( IF( `VS` !=0 AND (`PK`+`KM`+`D` < `PD`+`SK`+`G`),1,0)) AS Rain_Teams,
SUM( IF( `VS` !=0 AND (`PK`+`KM`+`D` = `PD`+`SK`+`G`) AND (`PK`+`KM`+`D` !=0),1,0)) AS Mixed_Teams,
SUM( IF( `VS` != 0 AND (`PK`+`KM`+`D` = 0) AND (`PD`+`SK`+`G` = 0),1,0)) AS Zero_Teams
               FROM (SELECT * FROM  `Styles_General` GROUP BY `ID`) AS baseview""")
for x in cursor.fetchall():
    Total_Teams=x[0]
    Non_Zero_Teams=x[1]
    Sun_Teams=x[2]
    Rain_Teams=x[3]
    Mixed_Teams=x[4]
    Zero_Teams=x[5]

if Sun_Teams+Rain_Teams+Zero_Teams+Mixed_Teams != Total_Teams:
    ofile.write("Something went wrong with totals")
else:
    ofile.write("--- Summary ---\n")
    ofile.write("Number of teams = "+ str(Total_Teams)+'\n')
    ofile.write("Number of teams w/spec = "+str(Non_Zero_Teams)+" , "+"{0:.2f}".format(Non_Zero_Teams/Total_Teams*100)+"%\n")
    ofile.write("Number of 'sun' teams = "+str(Sun_Teams)+" , "+"{0:.2f}".format(Sun_Teams/Total_Teams*100)+"%\n")
    ofile.write("Number of 'rain' teams = "+str(Rain_Teams)+" , "+"{0:.2f}".format(Rain_Teams/Total_Teams*100)+"%\n")
    ofile.write("Number of mixed teams = "+str(Mixed_Teams)+" , "+"{0:.2f}".format(Mixed_Teams/Total_Teams*100)+"%\n")
    ofile.write("Number of 'zero' teams = "+str(Zero_Teams)+" , "+"{0:.2f}".format(Zero_Teams/Total_Teams*100)+"%\n")

SELECT
AVG(if(`PK`+`KM`+`D` > `PD`+`SK`+`G`,`TROPHY`/(`PK`+`KM`+`D`)/`NPLAYER`,NULL)) AS Sun_Teams,
AVG(if(`PK`+`KM`+`D` < `PD`+`SK`+`G`,`TROPHY`/(`PD`+`SK`+`G`)/`NPLAYER`,NULL)) AS Rain_Teams,
AVG(if(`PK`+`KM`+`D` = `PD`+`SK`+`G`,`TROPHY`/(`PD`+`SK`+`G`)/`NPLAYER`,NULL)) AS Mixed_Teams
FROM(SELECT * FROM  `Styles_General` WHERE `VS` != 0 AND
(`PK`+`KM`+`D` != 0 OR `PD`+`SK`+`G` != 0) AND `TROPHY` > 0 AND `TROPHY` < 20) as baseview

Группировка по странам
SELECT
`COUNTRY`,
SUM(1) AS Total_Teams,
SUM(if(`PK`+`KM`+`D` > `PD`+`SK`+`G`,1,NULL)) AS Sun_Teams,
SUM(if(`PK`+`KM`+`D` < `PD`+`SK`+`G`,1,NULL)) AS Rain_Teams,
SUM(if(`PK`+`KM`+`D` = `PD`+`SK`+`G` AND `PD`+`SK`+`G` !=0,1,NULL)) AS Mixed_Teams,
SUM(if(`PK`+`KM`+`D` = `PD`+`SK`+`G` AND `PD`+`SK`+`G`=0,1,NULL)) AS Zero_Teams,
IF(SUM(if(`PK`+`KM`+`D` > `PD`+`SK`+`G`,1,NULL)) < SUM(if(`PK`+`KM`+`D` < `PD`+`SK`+`G`,1,NULL)),1,NULL) as Rain_Fed,
if(`PK`+`KM`+`D` < `PD`+`SK`+`G`,1,NULL) AS Rain_Spec_Dominate
FROM (SELECT * FROM  `Styles_General` WHERE `VS` != 0) as baseview
group by `COUNTRY`

Среднее число спецух

Среднее число трофеев на спецуху

Оспецушеннось игроков

Число трофеев на оспецушенность

Средняя сила по стилям
Среднее число игроков
Среднее число силы на спецуху
Среднее число трофеев на силу
Средняя позиция в дивизионе



Число команд разного стиля по странам
Место команды другого стиля в стране

#closing everything
ofile.close()
cursor.close()
database.close()
