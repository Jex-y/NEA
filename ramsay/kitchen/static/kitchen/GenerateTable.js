async function getItemOrders() {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };
    var response = await fetch("/api/orders/", requestOptions);
    return await response.json();
}

function onRowClick(id) {
    var myHeaders = new Headers();
    myHeaders.append("X-CSRFToken", csrftoken);

    var formdata = new FormData();
    formdata.append("id", id);

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: formdata,
        redirect: 'follow'
    };

    fetch("/api/orders/markcompleted", requestOptions)
        .then(response => response.text())
        .then(result => console.log(result))
        .catch(error => console.log('error', error));
}

function generateTableHead(table, keys) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of keys.slice(1)) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th)
    }

    let th = document.createElement("th");
    let text = document.createTextNode("completed");
    th.appendChild(text);
    row.appendChild(th)

}

function generateTable(table, data) {
    for (let element of data) {
        let row = table.insertRow();
        id = element.id;
        delete element.id;
        for (key in element) {
            let cell = row.insertCell();
            let text = document.createTextNode(element[key]);
            cell.appendChild(text)
        }
        let cell = row.insertCell();
        let btn = document.createElement("input");
        btn.type = "button";
        btn.className = "btn";
        btn.value = "Item Order Completed";
        let id_ = id;
        btn.onclick = function () { onRowClick(id_) };
        cell.appendChild(btn);
    }
}

function clearTable(table) {
    var rowCount = table.rows.length;
    for (var i = 1; i < rowCount; i++) {
        table.deleteRow(1);
    }
}

async function refreshTable(interval) {
    let table = document.getElementById('itemOrderTable');
    let data = await getItemOrders();
    let keys = Object.keys(data[0]);
    generateTableHead(table, keys);
    generateTable(table, data);

    let refresh = async function () {
        let data = await getItemOrders();
        clearTable(table);
        generateTable(table, data);
    }
    window.setInterval(refresh, interval);
}

refreshTable(5000);