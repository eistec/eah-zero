var http = require('http');

doGet = true
outMsg = '[{"bn":"tempservice","bt": '+(Math.floor(new Date().getTime() / 1000))+'},{"n":"3303/0/5700","v":-12.4},{"n":"3304/0/5700","v":14.0,"t":0.0}]'
var headers = {
    'Content-Type': 'application/json',
    'Content-Length': outMsg.length
};

var options = {
    host: '127.0.0.1',
    //path: '/datamanager/historian',
    //path: '/datamanager/historian/mulle-342',
    path: '/datamanager/historian/mulle-342/tempservice',
    port: 8461,
    method: 'GET'
    //method: 'PUT',
    //headers: headers
    };
    if (doGet == false){
        options.method = 'PUT'
        options.headers = headers
    }
    
    var callback = function(response) {
        console.log(`statusCode: ${response.statusCode}`)
        var str = '';
    
        response.on('data', function(chunk) {
            str += chunk;
        });
    
        response.on('end', function() {
            console.log(str);
        });
    };

    if (doGet) {
        console.log('Fetching data!')
        http.request(options, callback).end();
    } else {
        const req = http.request(options, callback);
        req.write(outMsg);
        req.end();
    }

    //https://nodejs.dev/learn/making-http-requests-with-nodejs