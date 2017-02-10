import rethinkdb as r
r.connect( "localhost", 28015).repl()
indexData=r.db("MF").table("latestdate").run()
value=0
date="12-Oct-2016";
for index in indexData:
    print(index.get("latestDateIndex"));
    value=index.get("latestDateIndex")+1;
print value
r.db("MF").table("datetable").insert({"date":date,"index":value}).run();
r.db("MF").table("latestdate").update({"latestDateIndex":value}).run();
