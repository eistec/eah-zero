var http = require('http');

doGet = true

function main() {
  outMsg = '[{"bn":"tempservice","bt": '+(Math.floor(new Date().getTime() / 1000))+'},{"n":"3303/0/5700","v":-2.4},{"n":"3304/0/5700","v":24}]'
  var headers = {
    'Content-Type': 'application/json',
    'Content-Length': outMsg.length
  };

  var options = {
    host: '127.0.0.1',
    //path: '/datamanager/historian',
    //path: '/datamanager/historian/mulle-342',
    //path: '/datamanager/historian/mulle-342/tempservice',
    path: '/datamanager/proxy/mulle-342/tempservice',
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
    console.log('Storing data!')
    const req = http.request(options, callback);
    req.write(outMsg);
    req.end();
  }

}


if (require.main === module) {
  main();
}
