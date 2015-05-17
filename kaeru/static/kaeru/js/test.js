
function List(){
	List.makeNode=function(){ 
		return {data:null,next:null};
	};
	this.start=null; 
	this.end=null;
	/*var data = null;
	var next= null;
	var start = null;
	var end = null;*/

	this.add=function (data){
		
		if(this.start===null){ 
			this.start=List.makeNode(); 
			this.end=this.start;
		}else{ 
			this.end.next=List.makeNode(); 
			this.end=this.end.next; 
		};
		this.end.data=data; 
	};

	this.remove = function(data) { 
		var current = this.start; 
		var previous = this.start; 
		while (current !== null) { 
			if (data === current.data) { 
				if (current === this.start) { 
					this.start = current.next; 
					return; 
				} 
				if (current === this.end) 
					this.end = previous;
				previous.next = current.next; return; 
			}
			previous = current; 
			current = current.next; 
		}
	}; 

	

	this.get = function(i) { 
		//alert(current.data)
		var current = this.start; 
		while (current !== null) { 
			
			if (i === 0)
				return current.data; 
			i--; 
			current = current.next; 
		} 
		return null; 
	}; 

	this.size = function(){
		var current = this.start;
		var i = 0;
		while(current != null){
			i++;
			current = current.next;
		}
		return i;
	};


}



function Map() {
    this.keys = new Array();
    this.data = new Object();

    this.put = function (key, value) {
        if (this.data[key] == null) {
            this.keys.push(key);
        }
        this.data[key] = value;
    };

    this.get = function (key) {
        return this.data[key];
    };

    this.remove = function (key) {
        this.keys.remove(key);
        delete this.data[key];
    };

    this.each = function (fn) {
        if (typeof fn != 'function') {
            return;
        }
        var len = this.keys.length;
        for (var i = 0; i < len; i++) {
            var k = this.keys[i];
            fn(k, this.data[k], i);
        }
    };

    this.entrys = function () {
        var len = this.keys.length;
        var entrys = new Array(len);
        for (var i = 0; i < len; i++) {
            entrys[i] = {
                key: this.keys[i],
                value: this.data[i]
            };
        }
        return entrys;
    };

    this.isEmpty = function () {
        return this.keys.length == 0;
    };

    this.size = function () {
        return this.keys.length;
    };
}


/*
 * Session management Code. Session class. Singleton.
 */
 var Session = (function(){

 	function Session(){
		//god knows what goes here
		//alert("ghost code");
		var serverTimeout = 6000; //10 mins
		var sessionTimeout = 18000; //default timeout = 20 mins
		var timeoutRedirectPage = '/login'; //default redirect page. can be rewritten by the setter
		var sessionVariables = new Map();
		this.setSessionTimeout=function(timeout){
			//alert("in setSessionTimeout method");
			this.sessionTimeout = timeout;
			

		};
		this.setTimeoutRedirectPage=function(redirectPage){
			this.timeoutRedirectPage = redirectPage;
		};
		this.setAttribute=function(key,value){
			this.sessionVariables.put(key,value);

		}
		this.getAttribute=function(key){
			return this.sessionVariables.get(key);
		}
		this.trackUserActivity = function(){
			var timer;
			var remainingTime = this.sessionTimeout;
			//this.sessionVariables = new Map();
			window.onload = resetTimer;
			window.onmousemove = resetTimer;
			window.onmousedown = resetTimer; 
			window.onclick = resetTimer;     
			window.onscroll = resetTimer;    
			window.onkeypress = resetTimer;
			function logout() {
		    	//alert("timeout caused");
		    	this.sessionVariables = null
		    	window.location.href = this.timeoutRedirectPage;

		    };

		    function sendKeepAliveProbe(){
		    	xmlhttp = new XMLHttpRequest();
		    	xmlhttp.onreadystatechange=function(){
		    		if(xmlhttp.readyState ==4 && xmlhttp.status==200)
		    			document.getElementById('ajaxtest').innerHTML = xmlhttp.responseText;
		    		else
		    			document.getElementById('ajaxtest').innerHTML = "<strong>waiting for response</strong>";
		    	}

		    	xmlhttp.open("GET","/keepAliveProbe",true)
		    	xmlhttp.send();

		    	remainingTime -= serverTimeout;
		    	resetTimer();
		    }

		    function resetTimer() {
		    	clearTimeout(timer);
		    	
		    	if(serverTimeout < remainingTime)
		        	timer = setTimeout(sendKeepAliveProbe, serverTimeout - 1000 );  // time is in milliseconds
		        else
		        	timer = setTimeout(logout, remainingTime);  // time is in milliseconds
		    };
		};
	}
	var instance;
	return {
		createSession : function(timeoutAtCreate,redirectPage){
			if(instance == null){
				

				instance = new Session();
				instance.setSessionTimeout(timeoutAtCreate*60*1000)
				instance.setTimeoutRedirectPage(redirectPage)
				instance.trackUserActivity();
				instance.constructor = null;
			}
			

			return instance;
		} 
	};

})();


function createType() {
	"use strict";
	//evt.preventDefault();
	
	var jsonString = document.getElementById("json").value;
	
	var primaryKeyName = "";
	//alert(jsonString);
	if(jsonString != "")
	{
		var obj = JSON.parse(jsonString);

		// var head = document.getElementsByTagName('head')[0]
		var script = document.createElement("script");
		var typeName = document.getElementById('typename');
		// Begin of main persistent data type creation
		script.innerHTML = "function "+typename.value+"(){ " ;

		for(var i=0;i<obj.fields.length;i++)
		{

			if(obj.fields[i].name != "")
			{
				alert(obj.fields[i].name);
				if(obj.fields[i].primary == true)
				{
					primaryKeyName = obj.fields[i].name ;
				}
				script.innerHTML += "var "+ obj.fields[i].name +";"+
				"this.set"+obj.fields[i].name+"=function(paramValue){" +
				" this."+obj.fields[i].name+"= paramValue;\n" +
				" //alert(this."+obj.fields[i].name+");\n}; \n" +

				"this.get"+obj.fields[i].name +"=function(){" +
				"return this."+obj.fields[i].name+"};" ;

			}	
		}



		//Begin of save()
		
		script.innerHTML +="\n this.save=function(){ \n"
		script.innerHTML += " var queryString = ''\n"
		for(var i=0;i<obj.fields.length;i++)
		{
			if(obj.fields[i].name != "")
			{
				script.innerHTML += "+" + 'this.get'+obj.fields[i].name+"() +','"
			}
		}
		script.innerHTML += "+ 'dummy' \n" //this field is important. Not removed while code clean-up
		
		script.innerHTML += "var xmlhttp = new XMLHttpRequest(); \n"
		script.innerHTML += "xmlhttp.onreadystatechange=function(){ \n"
		script.innerHTML += "if(xmlhttp.readyState ==4 && xmlhttp.status==200) \n"
		script.innerHTML += "document.getElementById('ajaxtest').innerHTML = xmlhttp.responseText; \n"
		script.innerHTML += "else \n"
		script.innerHTML += "document.getElementById('ajaxtest').innerHTML = '<strong>waiting for response</strong>'; \n"
		script.innerHTML += "	}\n"
		script.innerHTML += "xmlhttp.open('GET','/save_user_data?table="+typename.value+"&query='+queryString,true)\n"
		script.innerHTML += "xmlhttp.send();\n"
		script.innerHTML +="};"
		
		//End of save()
		script.innerHTML += "}" ; //End of the main persistent data type creation


		//Begin of QueryClass for the persistent data type
		script.innerHTML += "\nfunction "+typename.value+"Query(){"
		script.innerHTML += "this.get"+typename.value+"By"+primaryKeyName+" =  function(value){";
		script.innerHTML += "\n //implement code to  talk to Django here \n";
		script.innerHTML += "var xmlhttp = new XMLHttpRequest(); \n"
		script.innerHTML += "returnTypeObj = new "+typename.value+"(); \n"
		script.innerHTML += "xmlhttp.onreadystatechange=function(){ \n"
		script.innerHTML += "if(xmlhttp.readyState ==4 && xmlhttp.status==200){ \n"
		script.innerHTML += "document.getElementById('ajaxtest').innerHTML =xmlhttp.responseText; \n "
		script.innerHTML += "var responseStr = xmlhttp.responseText; \n"
		script.innerHTML += " var rowElements = responseStr.split(',') \n"
		
		for(var i=0;i<obj.fields.length;i++)
		{
			if(obj.fields[i].name != "")
			{
				script.innerHTML += " returnTypeObj.set"+obj.fields[i].name+"(rowElements["+i+"])\n"
			}
		}
		script.innerHTML += "}else \n"
		script.innerHTML += "document.getElementById('ajaxtest').innerHTML = '<strong>waiting for response</strong>'; \n"
		
		script.innerHTML += "	}//end of onreadystatechange function\n"
		script.innerHTML += "xmlhttp.open('GET','/get_type_data_by_key?table="+typename.value+"&key="+primaryKeyName+"&keyValue='+value,false)\n"
		script.innerHTML += "xmlhttp.send();\n"
		//script.innerHTML += "alert('query function called');"
		script.innerHTML += "return returnTypeObj; \n"
		script.innerHTML += "}//End of get<typename>By<PrimaryKeyName> method \n"
		script.innerHTML += "\n this.getAll"+typename.value+"=function(){\n"
		script.innerHTML += "var xmlhttp = new XMLHttpRequest(); \n"
		script.innerHTML += "resultList = new List(); \n"
		script.innerHTML += "result"+typename.value+" = new "+typename.value+"(); \n"
		script.innerHTML += "xmlhttp.onreadystatechange=function(){ \n"
		script.innerHTML += "if(xmlhttp.readyState ==4 && xmlhttp.status==200){ \n"
		script.innerHTML += "var responseStr = xmlhttp.responseText; \n"
		script.innerHTML += "document.getElementById('ajaxtest').innerHTML =xmlhttp.responseText; \n "
		script.innerHTML += "\n //code to parse return string and put it into the List type \n"
		script.innerHTML += "var resultRows = responseStr.split('$') \n"
		script.innerHTML += "//create the List of type <typename>. Also create Objects of <typename> and populate the read values \n"
		
		

		script.innerHTML += "for(var i=0; i< resultRows.length;i++){ \n"
		script.innerHTML += " var rowElements = resultRows[i].split(',') \n"
		script.innerHTML += "result"+typename.value+" = new "+typename.value+"(); \n"
		for(var i=0;i<obj.fields.length;i++)
		{
			if(obj.fields[i].name != "")
			{
				script.innerHTML += " result"+typename.value+".set"+obj.fields[i].name+"(rowElements["+i+"])\n"
			}
		}
		script.innerHTML += "resultList.add(result"+typename.value+")\n"
		
		script.innerHTML += "} //End of for loop of resultRows \n"
		script.innerHTML += "}//End of onreadystatechange if condition \n"
		script.innerHTML += "else \n"
		script.innerHTML += "document.getElementById('ajaxtest').innerHTML = '<strong>waiting for response</strong>'; \n"
		
		script.innerHTML += "	}//end of onreadystatechange function\n"
		script.innerHTML += "xmlhttp.open('GET','/get_all_type_data?table="+typename.value+"',false)\n"
		script.innerHTML += "xmlhttp.send();\n"
		
		script.innerHTML += "return resultList; \n"
		script.innerHTML += "} //End of getAll<typename> method \n"
		script.innerHTML += "} //End of <typename>Query class \n" ; 
		//End of QueryClass for the persistent data type
		alert(script.innerHTML)
		document.head.appendChild(script);
		//Call server to create the table and see what it returns
		//the fnction createTable() is for test purposes. Could be removed
		function createTable(){
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.onreadystatechange=function(){
				if(xmlhttp.readyState ==4 && xmlhttp.status==200)
					document.getElementById('ajaxtest').innerHTML = xmlhttp.responseText;
				else
					document.getElementById('ajaxtest').innerHTML = "<strong>waiting for response</strong>";
			}

			xmlhttp.open("GET","/create_test_tables",true)
			xmlhttp.send();

		}

		createTable();
	}
}

function testScript(){
	
	/* Sample code that could be used to test the APi
	var friend = new Friend();
	friend.setusername('MyFirstFriendName');
	friend.setpassword('abc@123')
	friend.save() // This will save the friend object back to the databse.
	
	var friendQuery = var FriendQuery();
	var friend_retrieve = friendQuery.getFriendByusername('MyFirstFriendName')
	alert(friend_retrieve.getpassword()) // should return abc@123

	var session = Session.createSession(10,'/Login'); // set the timeout to 10 mins
	session.setAttribute('loginTime','5/6/2015 00:00:00')

	alert(session.getAttribute('loginTime')) //Should return 5/6/2015 00:00:00

	var friendList = new List();
	friendList = friendQuery.getAllFriend();

	alert(friendList.get(0).getusername()); // should return the username of the first friend created and saved in the database
	*/
	eval(document.getElementById('codetest').value)


	
}





