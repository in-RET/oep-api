function init(){
    document.getElementById("submit_data").addEventListener("click", buildrequest);
}

function buildrequest() {
    const datapath = document.getElementById('datapath');

    fetch('http://localhost:8000/upload/localdata', {
        method: "POST",
        headers: {
            'accept': 'application/json',
        },
        body: new URLSearchParams({
            'datapath': datapath.value,
            'with_upload': false,
            'topic': 'sandbox'
        })
    }).then(res => console.log(res));
}