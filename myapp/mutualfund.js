var express = require('express');
var router = express.Router();
var tst = require('./app.js');


var jsonstring="";



/* GET Tail page. */
router.get('/getAllmutualFund', function(req, res, next) {
  //console.log(r)

   r.db('MF').table('AllMutualFund').run().then(function (result) {
       //console.log(JSON.stringify(result));
        res.send(JSON.stringify(result));
    
  });
  
});


router.get('/getmfNav', function(req, res, next) {
    res.setHeader('Access-Control-Allow-Headers', '*');
    res.setHeader('content-type', 'application/json');
    res.header('Access-Control-Allow-Origin', "*");
    //var mutualfundId=req.query.mfname;
    res.send("Hello");

});
module.exports = router;