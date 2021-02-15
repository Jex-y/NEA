async function getItemOrders() {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };
    var response = await fetch("/api/orders/", requestOptions);
    return await response.json();
}

"See https://www.valentinog.com/blog/html-table/"

function generateTableHead(table, keys) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of keys) {
        let th = document.createElement("th");
        let text = document.createTextNode(key);
        th.appendChild(text);
        row.appendChild(th)
    }
}

let table = document.getElementById('table');
let data = getItemOrders();
let keys = Object.keys(data[0]);
generateTableHead(table, keys);