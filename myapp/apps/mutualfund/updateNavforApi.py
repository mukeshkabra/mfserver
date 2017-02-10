#navdataApi
import rethinkdb as r
r.connect( "localhost", 28015).repl()
ida=r.db("MF").table("latestdate").run()
latestdateindex=0
currentdate=0
weekly=0
daily=0
for it in ida:
    latestdateindex=it.get("latestDateIndex")
ida=r.db("MF").table("datetable").filter(r.row["index"].eq(latestdateindex)).run()
for it in ida:
    currentdate=it.get("date")
print currentdate
ida=r.db("MF").table("averageNav").run()
for it in ida:
    code=it.get("code")
    idaa=r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).get_field("nav").get_field(currentdate).run()
    temp=idaa
    idaa=(list(temp))
    print idaa
    if len(idaa) is 0:
        print code +" Hello "  
    for i in idaa:
        print code +" : " +i
        weekleyidaa=r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).get_field("weekly").run()
        for widaa in weekleyidaa:
            weekly=widaa
        dailyidaa=r.db("MF").table("averageNav").filter(r.row["code"].eq(code)).get_field("In1Day").run()
        for dailydata in dailyidaa:
            daily=dailydata
        r.db("MF").table("navdataApi").filter(r.row["code"].eq(code)).update({"Nav":i,"weekly":weekly,"Lastday":daily}).run()
    
        
   
    
    
