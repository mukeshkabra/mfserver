var express = require('express');
var index = require('../../app.js');
var router = express.Router();
var app = index.app;
var io = index.io;
var connection = null;
var r = require('rethinkdb');
var async=require('async');

r.connect( {host: 'localhost', port: 28015}, function(err, conn) {
    if (err) throw err;
    connection = conn;
});
var path    = require("path");



/* GET Tail page. */



router.get('/getAllmutualFund', function(req, res, next) {

   r.db('MF').table('AllMutualFund').run(connection,function(err,result) {
       //console.log(JSON.stringify(result));
       result.toArray(function(err, result1) {
           if (err) throw err;
           console.log(JSON.stringify(result1, null, 2));
           res.send(JSON.stringify(result1));

       });

    
  });
  
});
router.get('/getsubMutualFund', function(req, res, next) {
  var pid=req.query.pId;
   r.db('MF').table('temp').filter(r.row("pId").eq(parseInt(pid))).run(connection,function(err,result) {
       //console.log(JSON.stringify(result));
       result.toArray(function(err, result1) {
        if (err) throw err;
          console.log(JSON.stringify(result1, null, 2));
          res.send(JSON.stringify(result1));


           

       });

    
  });
  
});
function cursorq(cursor,callback){

  console.log("cursor");
  cursor.each(function(error, row) {
      console.log(row)
      callback(row)

    });

}
function exeucteQuery(code,callback){
  var o={};
  var te={};
  var codes=[];
  var rawtemp=[];
  var pendings=code.length;
  var j=0
  for(var i in code){
      console.log("Hello"+i)
      r.db('MF').table('temp').filter(r.row("code").eq(code[i])).getField("info").getField("nav").run(connection).then(function(cursor){;
      cursor.each(function(error, row) {
      console.log("Hello"+row);
      //rawtemp.push(row);
      
      console.log(o)
      o[code[j]]=row;
      console.log(o)
      j=j+1;
      rawtemp.push(o);
      //rawtemp.push({code[i]: row})
      pendings=pendings-1;
      console.log(pendings);
      if( pendings==0 ) {
        callback(o)
      }

    });

  });
}
};


function getDate(callback){
  console.log("inside date");
  r.db('MF').table('latestdate').getField("date").run(connection).then(function(cursor){
    cursor.each(function(error,row){
      if(error){
        console.log("error");
      }
      console.log(row);
      callback(row);
    });
  });
}
  /*console.log("starting")
  r.db('MF').table('temp').filter(r.row("code").eq("120009")).getField("info").getField("nav").run(connection).then(function(cursor){;
  cursorq(cursor,function(err,result){
    console.log('The user hello', result)
  });
});
  callback(null, rowtemp)

}*/

      
router.post('/updatewatchlist', function(req, res, next) {
    var result_temp = [];
    res.setHeader('content-type', 'application/json');
    var tempa;

    console.log('body: ' + JSON.stringify(req.body));
    console.log(req.body.code[0])
    exeucteQuery(req.body.code,function(result){
      console.log(result);
      getDate(function(resultdate){
        console.log("get date");
        result["date"]=resultdate
        res.send(JSON.stringify(result));
      });
      
    });
    /*async.forEach(req.body.code,function(result,callback){
      console.log(result)
      exeucteQuery(function(err,result){
        console.log('I will be logged fourth');
        console.log('The user is', result)
      });*/
      //r.db('MF').table('temp').filter(r.row("code").eq(result)).getField("info").getField("nav").run(connection).then(functon(cursor))
      /*r.db('MF').table('temp').filter(r.row("code").eq("120009")).getField("info").getField("nav").run(connection).then(function(cursor,callback){
        cursor.each(function(error,row){
          console.log(row);
          result_temp.push(row);
        });
      });*/
  
  
    
  });


   /*for (var i=0;i<req.body.code.length;i++){
    console.log("Hello")
    r.db('MF').table('temp').filter(r.row("code").eq(req.body.code[i])).getField("info").getField("nav").run(connection).then(function(cursor){
      cursor.each(function(error, row) {
            console.log("temp")
            console.log(row);
            result_temp.push(row)
            res.send(JSON.stringify(result_temp));

            
        });
      //result.to
      //res.send(JSON.stringify(result));
    });

   }*


   //console.log(result_temp)
 });
   /*r.db('MF').table('temp').filter(r.row("pId").eq(parseInt("123"))).run(connection,function(err,result) {
       //console.log(JSON.stringify(result));
       result.toArray(function(err, result1) {
        if (err) throw err;
          console.log(JSON.stringify(result1, null, 2));
          res.send(JSON.stringify(result1));


           

       });

    
  });
  
});*/
router.get('/navhistory',function(req,res,next){
var pid=req.query.mcode;
var plan=req.query.plan;
var name=req.query.mname;
var dateIndex;
console.log(pid)
   r.db('MF').table('navdataApi').filter(r.row("code").eq(pid)).run(connection,function(err,result) {
       //console.log(JSON.stringify(result));
       result.toArray(function(err, result1) {
        if (err) throw err;
          console.log(JSON.stringify(result1, null, 2));
          res.send(JSON.stringify(result1));


           

       });

    
  });
});
router.get('/s',function(req,res,next){
var pid=req.query.pId;
var type=decodeURI(req.query.ty);
   r.db('MF').table('mutualfunnav').filter(r.row("pId").eq(parseInt(pid))).filter(r.row("type").eq(" Growth Option")).run(connection,function(err,result) {
       console.log(JSON.stringify(result));
       result.toArray(function(err, result1) {
           if (err) throw err;
          console.log(JSON.stringify(result1, null, 2));
          res.send(JSON.stringify(result1));


           

       });

    
  });
});

router.get('/gethistorydata',function(req,res,next){
  var pid=req.query.pId;
  console.log(pid)
  r.db('MF').table('averageNav').filter(r.row("code").eq(pid)).run(connection,function(err,result) {
       //console.log(JSON.stringify(result));
       result.toArray(function(err, result1) {
          if (err) throw err;
          console.log(JSON.stringify(result1, null, 2));
          res.send(JSON.stringify(result1));


           
        });
       });
});

router.get('/getLatestNav',function(req,res,next){
 var dt = new Date();
 var utcDate = dt.getDate()+"-Oct-"+dt.getUTCFullYear()
  res.send(utcDate);
});
router.get('/getMfondate',function(req,res,next){
  var code=req.query.pId;
  var date=req.query.date;
  console.log(code)
  console.log(date)
  res.setHeader('Access-Control-Allow-Headers', '*');
  res.setHeader('content-type', 'application/json');
  res.header('Access-Control-Allow-Origin', "*");
  temp={}
  r.db('MF').table('averageNav').filter(r.row("code").eq(code)).getField("nav").getField(date).run(connection).then(function(cursor){
      //console.log(cursor);
      cursor.toArray(function(error,result){
        if(error) throw error;
        console.log(result[0]);
        temp["nav"]=result[0]
        res.send(JSON.stringify(temp));

      });
    
  });
});

router.get('/getmfNav', function(req, res, next) {
    res.setHeader('Access-Control-Allow-Headers', '*');
    res.setHeader('content-type', 'application/json');
    res.header('Access-Control-Allow-Origin', "*");
    var mutualfundId=req.query.mfname;

});
module.exports = router;