

function buttonOnClick()
{
    var name = document.getElementById("Name").value;
    var message = document.getElementById("Message").value;
    var body = "Command=ADD*&*msgID=0*&*Name="+name+"*&*Message="+message;    

    sendRequest("POST", body,"ADD");
}

function deleteOnClick(msgid)
{
    var body = "Command=DELETE*&*msgID="+msgid;
    sendRequest("POST",body,"DELETE");
}

function doTheThing()
{
    sendRequest("GET","","");
}

function sendRequest(reqType, reqBody, com)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {

            if(reqType == "POST")
            {
                doTheThing();
            }
            else
            {
                var response = xhttp.responseText;
                //alert(response);
                response = JSON.parse(response);
                var count = Object.keys(response).length
                display = ""
                for (var messageId in response) 
                {
                    
                    display += "<div id ='"+messageId+"'><b>"+response[messageId].Name+": "+response[messageId].Message +"   </b><button onclick = \"deleteOnClick('"+messageId+"')\">Delete</button></div>"
                    
                }
                //alert(display)
                document.getElementById("response").innerHTML = display;
            }
            
        }
    };
    xhttp.open(reqType, "/~patels15/cgi-bin/chatServer.cgi", true);
    if(reqType == "POST")
    {
        xhttp.setRequestHeader("Content-type","text/plain");
        xhttp.send(reqBody);
    }
    else
    {
        xhttp.send();
    }
}

function Setup()
{
    // A function pointer/callback
    setInterval(doTheThing, 1000);

   // doTheThing();
}

