#!/usr/bin/env python2
#coding=utf-8
import urllib2
import re
import pymysql

database = pymysql.connect(host='localhost', port=8889, user='username', passwd='passwd', db='VSOL', charset='utf8')
cursor = database.cursor()

for i in range (24000,25200):
    Team_ID = i
    print Team_ID
    response = urllib2.urlopen('http://www.virtualsoccer.ru/roster.php?num='+str(Team_ID))
    html = response.read()
    #print html

    #find out the name of the team
    regex = re.compile('(.*)arial; FONT-SIZE:14px;(.*)>(.*)</div>',re.IGNORECASE)
    result=regex.findall(html)
    if result:
        Team_Name = result[0][2]
    #    print Team_Name
    else:
        Team_Name=0
    #check if Team_Name is non-zero - then try setting for long team names
    if len(str(Team_Name))==0:
        regex = re.compile('(.*)team_name(.*)">(.*)</span>',re.IGNORECASE)
        result=regex.findall(html)
        if result:
            Team_Name=result[0][2]
    #If Team_Name is still zero - then try setting for free teams
    if len(str(Team_Name))==0:
        regex = re.compile('(.*)arial; FONT-SIZE:14px;(.*)>(.*)<a',re.IGNORECASE)
        result=regex.findall(html)
        if result:
            Team_Name=result[0][2]

    #find out the country
    if Team_Name!=0:
        regex = re.compile('(.*)\((.*)\,\s(.*)\)')
        result=regex.findall(Team_Name)
        if result:
            Team_Country = result[0][2]
        #    print Team_Country
        else:
            Team_Country=0
    else:
        Team_Country=0

    #find out the division
    regex = re.compile ('(.*)v2champ(.*)\"\>(.*)\,\s(.*)(\</a)')
    result = regex.findall(html)
    if result:
        Team_Div = result[0][3]
    #    print Team_Div
    else:
        Team_Div=0

    #find out the Vs
    regex = re.compile ('(.*)Vs(.*)\<b>(\d*)(.*)\<i\>(\d*)(.*)\<i\>(\d*)(.*)\<i\>(\d*)',re.IGNORECASE)
    result = regex.findall(html)
    if result:
        Team_Vs = result[0][2]
        Team_Vs_Tot = result[0][4]
        Team_Vs_Cou = result[0][6]
        Team_Vs_Div = result[0][8]
    #    print Team_Vs, Team_Vs_Div
    else:
        Team_Vs=0
        Team_Vs_Tot=0
        Team_Vs_Cou=0
        Team_Vs_Div=0
    #print Team_Vs

    #find out the NPlayers
    regex = re.compile ('(.*)nPlayer(.*)\s(\d*);',re.IGNORECASE)
    result = regex.findall(html)
    if result:
        Team_NPlayers = result[0][2]
    #    print Team_NPlayers
    else:
        Team_NPlayers=0


    #find out the Cups
    regex = re.compile ('(.*)Трофеи(.*)\">(\d*)\<',re.UNICODE)
    result = regex.findall(html)
    if result:
        Team_Cups = result[0][2]
    #    print Team_Cups
    else:
        Team_Cups=0

    #----------------------------------------------------PK
    #find out the PKs
    N_PK=list()
    N_PKt=0
    for i in range(1,5):
        if i==1:
            regex = re.compile ('(.*)\"Пк\"(.*)',re.UNICODE)
        else:
            regex = re.compile ('(.*)\"Пк'+str(i)+'\"(.*)',re.UNICODE)
        result = regex.findall(html)
        if result:
            N_PK.append(len(result))
        else:
            N_PK.append(0)
        N_PKt += i*N_PK[i-1]
    #----------------------------------------------------PK

    #----------------------------------------------------KM
    #find out the KMs
    N_KM=list()
    N_KMt=0
    for i in range(1,5):
        if i==1:
            regex = re.compile ('(.*)\"Км\"(.*)',re.UNICODE)
        else:
            regex = re.compile ('(.*)\"Км'+str(i)+'\"(.*)',re.UNICODE)
        result = regex.findall(html)
        if result:
            N_KM.append(len(result))
        else:
            N_KM.append(0)
        N_KMt += i*N_KM[i-1]
    #----------------------------------------------------KM

    #----------------------------------------------------DR
    #find out the Ds
    N_DR=list()
    N_DRt=0
    for i in range(1,5):
        if i==1:
            regex = re.compile ('(.*)\"Д\"(.*)',re.UNICODE)
        else:
            regex = re.compile ('(.*)\"Д'+str(i)+'\"(.*)',re.UNICODE)
        result = regex.findall(html)
        if result:
            N_DR.append(len(result))
        else:
            N_DR.append(0)
        N_DRt += i*N_DR[i-1]
    #----------------------------------------------------DR

    #----------------------------------------------------PD
    #find out the PDs
    N_PD=list()
    N_PDt=0
    for i in range(1,5):
        if i==1:
            regex = re.compile ('(.*)\"Пд\"(.*)',re.UNICODE)
        else:
            regex = re.compile ('(.*)\"Пд'+str(i)+'\"(.*)',re.UNICODE)
        result = regex.findall(html)
        if result:
            N_PD.append(len(result))
        else:
            N_PD.append(0)
        N_PDt += i*N_PD[i-1]
    #----------------------------------------------------PD

    #----------------------------------------------------SK
    #find out the SKs
    N_SK=list()
    N_SKt=0
    for i in range(1,5):
        if i==1:
            regex = re.compile ('(.*)\"Ск\"(.*)',re.UNICODE)
        else:
            regex = re.compile ('(.*)\"Ск'+str(i)+'\"(.*)',re.UNICODE)
        result = regex.findall(html)
        if result:
            N_SK.append(len(result))
        else:
            N_SK.append(0)
        N_SKt += i*N_SK[i-1]
    #----------------------------------------------------SK

    #----------------------------------------------------GO
    #find out the GOs
    N_GO=list()
    N_GOt=0
    for i in range(1,5):
        if i==1:
            regex = re.compile ('(.*)\"Г\"(.*)',re.UNICODE)
        else:
            regex = re.compile ('(.*)\"Г'+str(i)+'\"(.*)',re.UNICODE)
        result = regex.findall(html)
        if result:
            N_GO.append(len(result))
        else:
            N_GO.append(0)
        N_GOt += i*N_GO[i-1]
    #----------------------------------------------------GO

    #--------Writing General-----------
    request = """insert into Styles_General
            (ID,NAME,COUNTRY,DIVISION,VS,VS_TOT,VS_COU,VS_DIV,TROPHY,NPLAYER,PK,KM,D,PD,SK,G)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (Team_ID,Team_Name,Team_Country,Team_Div,Team_Vs,Team_Vs_Tot,Team_Vs_Cou,Team_Vs_Div,Team_Cups,Team_NPlayers,N_PKt,N_KMt,N_DRt,N_PDt,N_SKt,N_GOt)
    cursor.execute(request,values)

    #--------Writing Detailed-----------
    request = """insert into Styles_Detailed
            (ID,PK1,PK2,PK3,PK4,KM1,KM2,KM3,KM4,D1,D2,D3,D4,PD1,PD2,PD3,PD4,SK1,SK2,SK3,SK4,G1,G2,G3,G4)
            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    values = (Team_ID,N_PK[0],N_PK[1],N_PK[2],N_PK[3],N_KM[0],N_KM[1],N_KM[2],N_KM[3],N_DR[0],N_DR[1],N_DR[2],N_DR[3],N_PD[0],N_PD[1],N_PD[2],N_PD[3],N_SK[0],N_SK[1],N_SK[2],N_SK[3],N_GO[0],N_GO[1],N_GO[2],N_GO[3])
    cursor.execute(request,values)

        #--------Writing HTML-----------
    #request = """insert into Raw_HTML(ID,HTML) values(%s, %s)"""
    #values = (Team_ID,html)
    #cursor.execute(request,values)

    database.commit()

cursor.close()
database.close()
