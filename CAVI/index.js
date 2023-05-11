JSC.Chart('chartDiv', {});

fetch('.\_out-put.csv')
   .then(function (response) {
      return response.text();
   })
   .then(function (text) {
	csvToSeries(text);
   })
   .catch(function (error) {
      //Something went wrong
      console.log(error);
   });

function csvToSeries(text) {
    let dataAsJson = JSC.csv2Json(text);
    console.log(dataAsJson)
}
