function reqListener() {
  console.log(this);
}

function getStock(opts, type) {
    var defs = {
        baseURL: 'https://finance.yahoo.com',
        query: '/quote/{stock}/history?',
        params: {
            period1: '1672531200',
            period2: '1675209600',
            interval: '1d',
            filter: 'history',
            frequency: '1d',
            includeAdjustedClose: 'true',
        },
    };

    opts = opts || {};

    if (!opts.stock) {
        complete('No stock defined');
        return;
    }

    var query = defs.query.replace('{stock}', opts.stock)
    defs.params.period1 = new Date(opts.startDate).valueOf() / 1000
    defs.params.period2 = new Date(opts.endDate).valueOf() / 1000
    var params = new URLSearchParams(defs.params).toString();

    var url = defs.baseURL + query + params;


    var xhttp = new XMLHttpRequest();
    xhttp.addEventListener("load", reqListener);
    xhttp.open("GET", url, true);
    xhttp.send();

}
window.getStock = getStock;


function test() {
    getStock({ stock: 'LYFT', startDate: '2023-01-01', endDate: '2023-02-01' }, 'historicaldata');
}
