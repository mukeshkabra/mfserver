import urllib2
import rethinkdb as r
import json
r.connect( "localhost", 28015).repl()
import json
ida=r.db("MF").table("averageNav").get_field("code").run()
al=[]
for i in ida:
    #print i
    al.append(i)
print len(al)

ida1=r.db("MF").table("temp").get_field("code").run()
al1=[]
for i in ida1:
    #print i
    al1.append(i)
print len(al1)

for i in al1:
    if i not in al:
        print i
        dicta={};
        ida=r.db("MF").table("mutualfunnav").filter(r.row["code"].eq(i)).run()
        for data in ida:
            dicta[data.get("dateofNav")]=data.get("nav")
        print "########"+i
        print dicta
        print "######"
        ra=json.dumps(dicta)
        loadedr=json.loads(ra)
        r.db("MF").table("averageNav").insert({"code":i,"nav":loadedr}).run()

        
             

