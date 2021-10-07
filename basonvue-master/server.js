var express = require('express');
var app = express();
/*var history = require('connect-history-api-fallback');
const staticFileMiddleware = express.static('dist');
const serveStatic = require('serve-static')*/
const path = require('path')

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "mon-domaine.fr"),
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept"),
    next()
})
app.use(express.static(__dirname+ '/dist'));

const port = process.env.PORT || 8080
app.listen(port)

/*
  "eslintConfig":{
    "root": true,
    "env":{
      "node": true
    },
    "extends":[
      "plugin:vue/vue3-recommended"
    ]
  },
A mettre dans package.json si on utilise le serveur.
  */ 