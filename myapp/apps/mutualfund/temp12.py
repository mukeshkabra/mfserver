import urllib2
import rethinkdb as r
r.connect( "localhost", 28015).repl()
import json
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
while(i<lenA):
    
    print i
    if(i>3):
        print "NAME = "+a[i].strip()
        if("Schemes" in a[i].strip()):
            print "Hello"
            i=i+2
            continue
        k=0
        ida=r.db("MF").table("AllMutualFund").filter(r.row["name"].eq(a[i].strip())).run()
        for row in ida:
            print(row.get("id"));
        print row.get("id")
        print type(row.get("id"))
        j=i+2
        if(j>(lenA-2)):
            break;
        else:
            stra=a[j].strip();
            while(j<lenA and (a[j].strip())!=""):
                
                print a[i].strip()+" Info "+a[j].strip()
                submutualfund=a[j].strip().split(";");
                schemaCode=submutualfund[0].strip();
                ISIN=submutualfund[1].strip();
                schemeName=submutualfund[3].strip();
                Nav=submutualfund[4].strip();
                date=submutualfund[7].strip();
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
                dicta["name"]=name
                dicta["plan"]=plan
                dicta["typemf"]=typemf
                dicta["nav"]=Nav
                ra=json.dumps(dicta)
                loadedr=json.loads(ra)
                r.db("MF").table("temp").insert({"code":schemaCode,"info":loadedr,"pId":row.get("id")}).run()
                if(check):
                    value=0;
                    indexData=r.db("MF").table("latestdate").run()
                    for index in indexData:
                        print(index.get("latestDateIndex"))
                        value=index.get("latestDateIndex")+1;
                    #r.db("MF").table("datetable").insert({"date":date,"index":value}).run();
                    #r.db("MF").table("latestdate").update({"latestDateIndex":value}).run();
                    check=False;





                    
                k=k+1
                j=j+1
            i=j+1
    else:
        i=i+1
    
        
   
