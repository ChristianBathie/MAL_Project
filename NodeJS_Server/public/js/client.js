/* var net = require('net');

var client = net.connect({port: 8081, host: '127.0.0.1'}, () => {
	console.log("connected.server");
	client.write("world!\r");
	console.log("Local Port: "+client.localPort);
	console.log("Remote Port: "+client.remotePort);
});
client.on('data', (data) => {
	console.log(data.toString());
	client.end();
});
client.on('end', () => {
	console.log("disconnected from server");
}); */

var sortKey = "id";

function getUsers()
{
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			tableData = JSON.parse(this.responseText);
			populateTable(tableData.users);
		}
	};
	xhttp.open("GET", "/json/users.json", true);
	xhttp.send();
}

function postUser()
{
	var name = document.forms["addUserForm"]["name"].value;
	var pass = document.forms["addUserForm"]["pass"].value;
	var prof = document.forms["addUserForm"]["comp"].value;
	var postStr = "name=" + encodeURIComponent(name) + "&pass=" + encodeURIComponent(pass) + "&comp=" + encodeURIComponent(prof);
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			tableData = JSON.parse(this.responseText);
			jsonTable = document.getElementById("jsonTable");
			jsonTable.setAttribute("data-items",JSON.stringify(tableData.users));
			sortTable(sortKey);
		}
	};
	xhttp.open("POST", "/addUser", true);
	xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	xhttp.send(postStr);
	//document.getElementById("postData").innerHTML = postStr;
	document.forms["addUserForm"].reset();
	return false;// prevent page reloading
}

function populateTable(users)
{
	//tableData = JSON.parse(jsonResponse);
	//users = tableData.users;
	//document.body.innerHTML = JSON.stringify(users);
	
	jsonTable = document.getElementById("jsonTable");
	jsonTable.setAttribute("data-items",JSON.stringify(users));
	jsonTableBody = document.getElementById("jsonTableBody");
	jsonTableBody.innerHTML = "";
	
	//document.body.innerHTML = JSON.stringify(tableData.users[1]);
	//jsonTable.innerHTML = "<tr> <th>ID</th><th>Name</th><th>Password</th><th>Profession</th> </tr>";
	for (i=0;i<users.length;i++) {
		row = document.createElement("tr");
		cellID = document.createElement("td");
		cellName = document.createElement("td");
		cellPass = document.createElement("td");
		cellProf = document.createElement("td");
		textID = document.createTextNode(users[i]['id']);
		textName = document.createTextNode(users[i]['name']);
		textPass = document.createTextNode(users[i]['password']);
		textProf = document.createTextNode(users[i]['company']);
		cellID.appendChild(textID);
		cellName.appendChild(textName);
		cellPass.appendChild(textPass);
		cellProf.appendChild(textProf);
		row.appendChild(cellID);
		row.appendChild(cellName);
		row.appendChild(cellPass);
		row.appendChild(cellProf);
		jsonTableBody.appendChild(row);
	}
}

function sortTable(key)
{
	sortKey = key;
	jsonTable = document.getElementById("jsonTable");
	users = JSON.parse(jsonTable.getAttribute("data-items"));
	//document.getElementById("postData").innerHTML = users[0]["name"];
	//users = jsonData.users;
	mergeSort(users,sortKey);
	populateTable(users);
}

function dropMergeSort(a,key)
{
	var sortedArr = [];
	var unsortedArr = [];
	if(a.length < 2)
		return;
	if (a[0][key]<=a[1][key]) {
		sortedArr.push(a[0]);
		if (a[1][key]<=a[2][key])
			sortedArr.push(a[1]);
		else
			unsortedArr.push(a[1]);
	}
	else {
		unsortedArr.push(a[0]);
		sortedArr.push(a[1]);
	}
	for(i=2;i<a.length;i++){
		if (a[i][key] < a[sortedArr.length-1][key])
			unsortedArr.push(a[i]);
		else
			sortedArr.push(a[i]);
	}
	mergeSort(unsortedArr);
	m = sortedArr.length-1;
	a = sortedArr.concat(unsortedArr);
	merge(a, sortedArr, key, 0, m, sortedArr.length);
}

function mergeSort(a,key)
{
	if (a.length < 2)
		return;
	var arraySize = a.length;
	var aux = new Array(arraySize);
	for (var blockSize=1; blockSize<arraySize; blockSize*=2){
		for (var i=0; i<arraySize; i+=2*blockSize){
			mid = Math.min(i+blockSize-1, arraySize-1);
			j = Math.min(i+2*blockSize-1, arraySize-1);
			merge(a, aux, key, i, mid, j);
		}
	}
}

// a = array being sorted
// aux = auxilary array to temporarily hold values being sorted
// key = the key to the value being used for sorting comparisons
// i = left-most index of section being sorted (first index of left partition)
// m = center/pivot of section being sorted (last index of left partion)
// j = right-most index of section being sorted (last index of right partition)
function merge(a,aux,key,i,m,j)
{
	p = i;	// index for a[i]...a[m]
	q = m+1;// index for a[m+1]...a[j]
	r = i; 	// index of array c
	while (p<=m && q<=j) {
		if (a[p][key]<=a[q][key]) {
			aux[r] = a[p];
			p++;
		}
		else {
			aux[r] = a[q];
			q++;
		}
		r++;
	}
	while (p<=m) {
		aux[r] = a[p];
		p++;
		r++;
	}
	while (q<=j) {
		aux[r] = a[q];
		q++;
		r++;
	}
	for (r=i;r<=j;r++)
		a[r]=aux[r];
}

// quicksort works because at the end of each partition, the 'pivot' value wiil be in the correct spot, with everything smaller than it on the left, and everything larger on the right
function quickSort(a,key)
{
	i = 0;
	j = a.length-1;
	quickR(a,key,i,j);
}

function quickSortI(a,key)
{
	var stack = [];
	var i = 0;
	var j = a.length-1;
	if (i<)
	var p = partition(a,key,i,j);
	stack.push(p);
	while (stack.length>0){
		p = stack.pop();
		pLeft = partition(a,key,i,p-1);
		pRight = partition(a,key,p+1,j);
	}
	
}

function quickR(a,key,i,j)
{
	if (i<j) {
		p = partition(a,key,i,j);
		quickR(a,key,i,p-1);
		quickR(a,key,p+1,j);
	}
}

function partition(a,key,i,j)
{
	val = a[i][key];
	h = i;
	for (k=i+1;k<=j;k++) {
		if (a[k][key]<val) {
			h=h+1;
			temp = a[h];
			a[h] = a[k];
			a[k] = temp;
		}
	}
	temp = a[i];
	a[i] = a[h];
	a[h] = temp;
	return h;
}



