import  rethinkdb as r
import json
import time
r.connect("localhost",28015).repl()
latestDateIndex=0
latestNavdate=0
latestdate=r.db("MF").table("latestdate").get_field("latestDateIndex").run();
for t in latestdate:
    latestDateIndex=t

latestdate=r.db("MF").table("datetable").filter(r.row["index"].eq(latestDateIndex)).run();
for t in latestdate:
    print t.get("date")
    latestNavdate=t.get('date')


pattern = '%d-%b-%Y'
epoch = int(time.mktime(time.strptime(latestNavdate, pattern)))
print epoch

def weeklydate(dicta,latestNavdateepoch):
    print latestNavdateepoch
    keys=dicta.keys();
    print keys
    check=True;
    i=7
    temp=keys[0]
    while check:
        oneweekdate=time.strftime("%d-%b-%Y", time.localtime(epoch-(86400*i)))
        print "Hello One week "+oneweekdate
        if oneweekdate in keys:
            print "Hello " +oneweekdate
            check=False;
            break;
        else:
            print "Inside elese"
            i=i-1
        if i<0:
            oneweekdate=temp
            check=False;
    return dicta[oneweekdate];







ida=r.db("MF").table("mutualfunnav").get_field("code").distinct().run();
print len(ida)
for isin in ida:
    #print isin
    if(isin!="-"):
        print isin
        data=r.db("MF").table("mutualfunnav").filter(r.row["code"].eq(isin)).distinct().run()
        #print data
        dicta={}
        for a in data:
            print a.get("dateofNav")+" "+a.get("nav")
            #if (a.get("nav").encode('utf-8'))!="0.0000" or a.get("nav")!="0":
            if a.get("nav")!="N.A.":
                tempfloat=float(a.get("nav").encode('utf-8'))
                print tempfloat
                if tempfloat!=0.0:
                    temp=a.get("dateofNav")
                    dicta[temp]=a.get("nav")
        if (len(dicta))!=0:
            print dicta;
            ra=json.dumps(dicta)
            print ra
            loadedr = json.loads(ra)
            print loadedr
            weekdate=weeklydate(dicta,epoch)
            print weekdate
            if latestNavdate in dicta.keys():
                temp1=float(dicta[latestNavdate])-float(weekdate)
            else:
                temp1=float(weekdate)
            
            temp2=float(weekdate)
    
            percentage=(float(temp1)*100/float(temp2))
            print percentage
            
            r.db("MF").table("averageNav").insert({"code":isin,"nav":loadedr,"weekly":percentage}).run()


 
    
    
    
    
    
    
