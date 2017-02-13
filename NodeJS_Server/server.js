/* var net = require('net');

var server = net.createServer((socket) => {
	console.log("client connected");
	console.log(socket.address());
	socket.on('end', () => {console.log("client disconnected")});
	socket.write("hello\r");
	socket.pipe(socket);
});

server.on('error', (err) => {throw err;});

server.listen(8081, '127.0.0.1',() => {console.log("server bound");});

setTimeout(() => {server.close();}, 10000); */




/* var http = require('http');
var fs = require('fs');
var url = require('url');

var server = http.createServer((request, response) => {
	
	var reqURL = url.parse(request.url);// creates a url object (an object with conveniance methods for accessing sections of the url string)
	var pathname = reqURL.pathname;//should be done on above line so no excess variable assignment is needed
	
	console.log("client request recieved for: " + pathname);
	
	fs.readFile(pathname.substr(1), (err, data) => {
		if (err) {
			console.log(err);
			// HTTP Status: 404 - NOT FOUND
			// Content Type: text/plain
			response.writeHead(404, {'Content-Type': 'text/html'});
		}
		else { // Page found
			// HTTP Status: 200 - OK
			// Content-Type: text/plain
			if (pathname.slice(-4) == '.css')
				response.writeHead(200, {'Content-Type': 'text/css'});
			else
				response.writeHead(200, {'Content-Type': 'text/html'});
			// Write the content of the file to response body
			response.write(data.toString());
		}
		// Send the response body
		response.end();
	});
	
});
server.listen(8081, '127.0.0.1', () => {console.log("server bound and ready")});*/


/* var express = require('express');
var app = express();

app.use(express.static('public', {'extensions':['html']}));

// This responds with "Hello World" on the homepage
app.get('/', function (req, res) {
   console.log("Got a GET request for the homepage");
   res.send('Hello GET');
});

// This responds a POST request for the homepage
app.post('/', function (req, res) {
   console.log("Got a POST request for the homepage");
   res.send('Hello POST');
});

// This responds a DELETE request for the /del_user page.
app.delete('/del_user', function (req, res) {
   console.log("Got a DELETE request for /del_user");
   res.send('Hello DELETE');
});

// This responds a GET request for the /list_user page.
app.get('/list_user', function (req, res) {
   console.log("Got a GET request for /list_user");
   res.send('Page Listing');
});

// This responds a GET request for abcd, abxcd, ab123cd, and so on
app.get('/ab*', function(req, res) {   
   console.log("Got a GET request for /ab*");
   res.send('Page Pattern Match');
});

var server = app.listen(8081, function () {

   var host = server.address().address;
   var port = server.address().port;

   console.log("Example app listening at http://%s:%s", host, port)
}); */


/* var express = require('express');
var app = express();
var bodyParser = require('body-parser');

// Create application/x-www-form-urlencoded parser
var urlencodedParser = bodyParser.urlencoded({ extended: false });

app.use(express.static('public', {'extensions':['html']}));

app.get('/', function (req, res) {
	res.sendFile( __dirname + '/public/form_test.html');
});

app.post('/form_results', urlencodedParser, function (req, res) {
   // Prepare output in JSON format
   response = {
      first_name:req.body.first_name,
      last_name:req.body.last_name,
	  gender:req.body.gender
   };
   console.log(response);
   res.end("POST\n"+JSON.stringify(response));
});

app.get('/form_results', urlencodedParser, function (req, res) {
   // Prepare output in JSON format
   response = {
      first_name:req.query.first_name,
      last_name:req.query.last_name,
	  gender:req.query.gender
   };
   console.log(response);
   res.end("GET\n"+JSON.stringify(response));
});

var server = app.listen(8081, function () {
   var host = server.address().address;
   var port = server.address().port;
   
   console.log("Example app listening at http://%s:%s", host, port);

}); */



/* var express = require('express');
var app = express();
var fs = require("fs");

var bodyParser = require('body-parser');
var multer  = require('multer');
var upload = multer({ dest: 'public/tmp/'});

app.use(express.static('public',{'extensions':['html']}));
app.use(bodyParser.urlencoded({ extended: false }));
//app.use(upload);

app.get('/', function (req, res) {
	res.sendFile( __dirname + "/public/" + "upload_form.html" );
})

app.post('/file_upload', upload.single('uploadedFile'), function (req, res) {
	//console.log(req.file);
	console.log("Filename: "+req.file.filename);
	console.log("Path: "+req.file.path);
	console.log("MIME: "+req.file.mimetype);
	console.log("Encoding: "+req.file.encoding);
	
	response = {
		message:'File uploaded successfully',
		originalname:req.file.originalname,
		filename:req.file.filename
	};
	console.log( response );
	res.end( JSON.stringify( response ) );
	

})

var server = app.listen(8081, function () {
	var host = server.address().address
	var port = server.address().port

	console.log("Example app listening at http://%s:%s", host, port)
}) */



/* var express      = require('express');
var cookieParser = require('cookie-parser');

var app = express();
app.use(cookieParser());

app.get('/', function(req, res) {
   console.log("Cookies: ", req.cookies);
});
app.listen(8081); */


var express = require('express');
var bodyParser = require('body-parser');
var fs = require('fs');

var app = express();
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(__dirname + '/public', {'extensions':['html']}));

app.post('/addUser', function (req, res) {
	console.log("add user request recieved");
	fs.readFile(__dirname + '/public/json/users.json', 'utf8', function (err, data){
		if (err){
			console.log(err);
		} else {
		var obj = JSON.parse(data);
		var newID = 0;
		
		if (obj.users.length != 0)
			newID = obj.users[obj.users.length-1].id + 1;
		newUser = {
			id: newID,
			name: req.body.name,
			password: req.body.pass,
			company: req.body.comp
		}
		obj.users.push(newUser);
		json = JSON.stringify(obj);
		console.log(newUser);
		fs.writeFile(__dirname + '/public/json/users.json', json, 'utf8', function (err){
			if (err){
				console.log(err);
			} else {
			res.type('json');
			res.end( json );
		}}); // write it back 
	}});
});

var server = app.listen(8081, function () {

	var host = server.address().address
	var port = server.address().port

	console.log("Example app listening at http://%s:%s", host, port)

})
