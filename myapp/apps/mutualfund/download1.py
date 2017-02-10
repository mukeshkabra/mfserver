import urllib2
import rethinkdb as r
r.connect( "localhost", 28015).repl()
import json,time
response=urllib2.urlopen("http://portal.amfiindia.com/spages/NAV0.txt")
#print response.info()
#print response.read()
id=1;
a=response.read().strip().splitlines();
b=[];
j=0;
#print a
lenA=len(a)
i=0
#for i in range(len(a)):
rowid=0
k=0
check=True;
count=0
def calculateWeekley(date,dicta,weekdate):
    percentage=0
    print "date",date
    if dicta[date]!="N.A.":
        if date in dicta.keys():
            temp1=float(dicta[date])-float(dicta[weekdate])
        else:
            temp1=float(dicta[weekdate])
        if dicta[weekdate]!="N.A." and dicta:
            temp2=float(dicta[weekdate])
            tempfloat=float(temp2)
            temp2=tempfloat
            if temp2!=0.0:
                percentage=(float(temp1)*100/float(temp2))
            print percentage
    return percentage

    
def updateNavInAvg(nav,date,code):
    r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).update({"nav":{date:nav}}).run()

def weekleyUpdate(nav,date,code):
    pattern = '%d-%b-%Y'
    epoch = int(time.mktime(time.strptime(date, pattern)))
    print epoch
    ida=r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).run()
    dicta={}
    oneweekdate=0
    
    for it in ida:
        #print it.get("nav").keys()
        dicta=it.get("nav")
        print dicta
        keys=it.get("nav").keys()
        check1=True
        i=7
        while check1:
            
            oneweekdate=time.strftime("%d-%b-%Y", time.localtime(epoch-(86400*i)))
            #print "Hello One week "+oneweekdate
            if oneweekdate in keys:
                print "Hello " +oneweekdate
                check1=False;
                break;
            else:
                i=i-1
            if i<0:
                oneweekdate=nav
                check1=False
            
    if len(dicta)>0:
        print "Hello test" +oneweekdate
        print dicta[oneweekdate]
        #return oneweekdate
        percentage=calculateWeekley(date,dicta,oneweekdate)
        r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).update({"weekly":percentage}).run()

        

def dailyUpdate(nav,date,code):
    print nav
    pattern = '%d-%b-%Y'
    epoch = int(time.mktime(time.strptime(date, pattern)))
    print epoch
    ida=r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).run()
    dicta={}
    oneweekdate=0
    
    for it in ida:
        #print it.get("nav").keys()
        dicta=it.get("nav")
        print dicta
        keys=it.get("nav").keys()
        print keys
        check1=True
        i=1
        while check1:
            
            oneweekdate=time.strftime("%d-%b-%Y", time.localtime(epoch-(86400*i)))
            print "Hello One week "+oneweekdate
            if oneweekdate in keys:
                print "Hello " +oneweekdate
                check1=False;
                break;
            else:
                i=i+1
            if i<3:
                oneweekdate=date
                check1=False
            
    if len(dicta)>0:
        print "Hello test" +oneweekdate
        print dicta[oneweekdate]
        #return oneweekdate
        #percentage=calculateWeekley(date,dicta,oneweekdate)
        r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).update({"In1Day":dicta[oneweekdate]}).run()

    





while(i<lenA):
    
    print i
    if(i>3):
        #print "NAME = "+a[i].strip()
        if("Schemes" in a[i].strip()):
            print "Hello"
            i=i+2
            continue
        k=0
        ida=r.db("MF").table("AllMutualFund").filter(r.row["name"].eq(a[i].strip())).run()
        #for row in ida:
            #print(row.get("id"));
        #print row.get("id")
        #print type(row.get("id"))
        j=i+2
        if(j>(lenA-2)):
            break;
        else:
            stra=a[j].strip();
            while(j<lenA and (a[j].strip())!=""):
                
                #print a[i].strip()+" Info "+a[j].strip()
                submutualfund=a[j].strip().split(";");
                schemaCode=submutualfund[0].strip();
                ISIN=submutualfund[1].strip();
                schemeName=submutualfund[3].strip();
                Nav=submutualfund[4].strip();
                date=submutualfund[7].strip();
                count=count+1;
                if("-" in schemeName):
                    temp=schemeName.split("-")
                    if(len(temp)==3):
                        name=temp[0].strip()
                        plan=temp[1].strip()
                        typemf=temp[2].strip()
                    else:
                        name=temp[0].strip()
                        plan="NA"
                        typemf=temp[1].strip()
                else:
                    name=schemeName.strip()
                    plan="NA"
                    typemf="NA"


                dicta={}
                dicta["name"]=name.strip()
                dicta["plan"]=plan.strip()
                dicta["typemf"]=typemf.strip()
                dicta["nav"]=Nav.strip()
                ra=json.dumps(dicta)
                loadedr=json.loads(ra)
                ##r.db("MF").table("mutualfunnav").insert({"pId":row.get("id"),"mfId":k,"name":name,"plan":plan,"type":typemf,"nav":Nav,"code":schemaCode,"ISIN":ISIN,"dateofNav":date}).run()
                r.db("MF").table("temp").filter(r.row["code"].eq(schemaCode)).update({"rank":1,"info":{"nav":Nav}}).run()
                r.db("MF").table("temp").filter(r.row["code"].eq(schemaCode)).update({"navdate":date}).run()
                ##r.db("MF").table("temp").insert({"code":schemaCode,"info":loadedr,"pId":row.get("id")}).run()

                updateNavInAvg(Nav,date,schemaCode)
                weekleyUpdate(Nav,date,schemaCode)
                print schemaCode
                dailyUpdate(Nav,date,schemaCode)
                if(check):
                    value=0;
                    indexData=r.db("MF").table("latestdate").run()
                    for index in indexData:
                        print(index.get("latestDateIndex"))
                        value=index.get("latestDateIndex")+1;
                    r.db("MF").table("datetable").insert({"date":date,"index":value}).run();
                    r.db("MF").table("latestdate").update({"latestDateIndex":value}).run();
                    r.db("MF").table("latestdate").update({"date":date}).run()
                    check=False;





                    
                k=k+1
                j=j+1
            i=j+1
    else:
        i=i+1

print "Count %d",(count)        
