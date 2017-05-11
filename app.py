from flask import Flask, render_template, request, send_file
import numpy
import pandas
import datetime
import glob
import sqlite3
import os

dbname = "schmeatodb.db"

#http://stackoverflow.com/questions/40294705/jquery-ui-sortable-save-to-database-with-python-flask-sqlite


#APTO
aptotable = "aptoschema"
conn=sqlite3.connect(dbname)
cur=conn.cursor()
df = pandas.read_csv('salesforce_object_metadata_2017_02_01.csv',index_col="FIELD_NAME",encoding='utf-8', low_memory=False)
df.to_sql(aptotable,conn, if_exists='replace')
conn.close()

app=Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/success-table', methods=['POST'])
def success_table():
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    global filename
    global tablename
    if request.method=="POST":
        file=request.files['file']
        #print(file.filename)
        extension = file.filename.split('.')[1]
        filename = file.filename.split('.')[0]
        if extension == 'csv':
            df = pandas.read_csv(file, encoding='utf-8', low_memory=False)
            #return pd.read_csv(filePath, encoding='cp437', low_memory=False)

        elif extension == 'xlsx':
            df = pandas.read_excel(file, encoding='utf-8')

        elif extension == 'xls':
            df = pandas.read_excel(file, encoding='utf-8')

        else:
            print("Did not load")

        try:
            #print(df.head(2))
            tablename = filename.replace(' ', '_')
            df.to_sql(tablename,conn, if_exists='replace')
            head=df.head(3)
            return render_template("index.html", text=head.to_html(), btn='mapfile.html')
            conn.close()
        except:
            return render_template("index.html", text="Sorry, something is not right!")
            conn.close()






@app.route("/map-file/")
def mapfile():
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()

    df = pandas.read_sql_query("SELECT * FROM {}".format(tablename) ,conn)
    
    clientheader = list(df.columns.values)[1:]
    c_divtext = list(enumerate(clientheader, start=1))
    c_divid = []
    for item in c_divtext:
        temp = "CH"+str(item[0])
        c_divid.append(temp)
    global clientdiv
    clientdiv = zip(c_divid, clientheader)


    #COMPANY ONLY
    df2 = pandas.read_sql_query("SELECT FIELD_NAME, OBJECT_LABEL FROM {} WHERE OBJECT_NAME = 'Account'".format(aptotable) ,conn)
    dfI = df2.set_index("FIELD_NAME")

    dfT = dfI.transpose()
    aptoheader = list(dfT.columns.values)[1:]
    #print(aptoheader)
    a_divtext = list(enumerate(aptoheader, start=1))
    a_divid = []
    for item in a_divtext:
        temp = "AH"+str(item[0])
        a_divid.append(temp)
    global aptodiv
    aptodiv = zip(a_divid, aptoheader)
    
    return render_template("mappage.html", clientdiv=clientdiv, aptodiv=aptodiv)
    conn.close()



if __name__=="__main__":
    app.run(debug=True)