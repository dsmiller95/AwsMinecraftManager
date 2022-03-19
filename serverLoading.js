const bootUrl = "https://6wtimpg3d7.execute-api.us-west-2.amazonaws.com/start_server";
const responseBox = document.getElementById("reloadResponse");
const reloadButton = document.getElementById("reloadButton");

async function AttemptBootServer(){
	let message;
	try{
		const responseMessage = await fetch(bootUrl, {
			method: "GET",
			//mode: 'no-cors', // no-cors, *cors, same-origin
		}).then((r)=>r.json());
		
		if(responseMessage.previousState == "running")
			message = "Server is already running, nothing changed. give the server a few minutes to become visible in minecraft server browser. If the server has not been visible after 5 minutes, please alert the system administrator";
		if(responseMessage.previousState == "pending")
			message = "Server is starting up, be patient";
		message = "Server booting. wait a few minutes and the server should be accessible";
	}catch(e){
		message = "Error: " + JSON.stringify(e);
	}
	
	responseBox.textContent = message;
}
reloadButton.onclick = AttemptBootServer;
