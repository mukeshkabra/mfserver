import urllib2
import rethinkdb as r
r.connect( "localhost", 28015).repl()
response=urllib2.urlopen("http://portal.amfiindia.com/spages/NAV0.txt")
#print response.info()
#print response.read()
id=1;
a=response.read().split("\n");
b=[];
for i in range(len(a)):
    if "Mutual Fund" in a[i] and "Dundee" not in a[i]:
        print a[i]
        if a[i] not in b:
            b.append(a[i])
            r.db("MF").table("AllMutualFund").insert({"name":a[i].strip(),"id":id}).run()
            id=id+1
