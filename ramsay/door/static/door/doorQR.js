var qr;
(function () {
    qr = new QRious({
        element: document.getElementById('qr-code'),
        size: 256,
        value: ''
    });
})();

async function getNewSession(table_num) {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/x-www-form-urlencoded");
    myHeaders.append("X-CSRFToken", csrftoken);

    var urlencoded = new URLSearchParams();
    urlencoded.append("table_num", table_num);

    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: urlencoded,
        redirect: 'follow'
    };

    try {
        var response = await fetch("/api/sessions/new", requestOptions);
        var json_data = await response.json();
        console.log(json_data.info);
        return json_data.sessid;
    } catch (expt) {
        console.error(expt);
        return "";
    }
}

async function generateQRCode() {
    var sessid = await getNewSession(document.getElementById('table-no').value);
    console.log(sessid)
    document.getElementById("qr-result").innerHTML = "Session ID:" + sessid;
    qr.set({
        foreground: 'black',
        size: 256,
        value: sessid
    });
}