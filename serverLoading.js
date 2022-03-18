async function AttemptBootServer(){
    var bootUrl = "https://6wtimpg3d7.execute-api.us-west-2.amazonaws.com/start_server";


    var mesage = "error";
    try{
        const response = await fetch(bootUrl, {
            method: 'GET',
            
            //mode: 'no-cors', // no-cors, *cors, same-origin
        });
    
        var responseMessage = response.json();
    
        if(responseMessage.previousState == "running"){
            message = "server is already running, nothing changed. give the server a few minutes to become visible in minecraft server browser. If the server has not been visible after 5 minutes, please alert the system administrator";
        }
        if(responseMessage.previousState == "pending"){
            message = "server is starting up, be patient";
        }
        message = "server booting. wait a few minutes and the server should be accessible";
    }catch(e){
        message = JSON.stringify(e);
    }

    var responseBox = document.getElementById("reloadResponse");
    responseBox .textContent     = message;
    
}

var reloadButton = document.getElementById("reloadButton");
reloadButton.onclick = AttemptBootServer;