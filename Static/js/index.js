//#region ** Loader Method **

var $loading = $('#uprogBusyIndicator').hide();
$(document)
  .ajaxStart(function () {
    $loading.show();
  })
  .ajaxStop(function () {
    $loading.hide();
  });

//#endregion

//#region  ** PageLoad Methods ** 

$(document).ready(function () {
    $("#btnPredictPersonalityHandler").click(GetPredictPersonalityHandler);
    return false;
  });
  
//#endregion

//#region Prediction 

function GetPredictPersonalityHandler(){
    let userJD = document.getElementById('txtJobDescription').value
    $.ajax({
        type: "GET",
        url: "/predict_personality",
        dataType: 'JSON',
        data: {
            userJD: userJD
        },
        success: function (data) {
            debugger
            //tblPersonalityPredicted
            for (let i = 0; i < Object.keys(data.Result).length; i++) {
                var tableRow ='<tr><td>' + Object.values(data.Result)[i].opennessCount + '</td><td>'+ Object.values(data.Result)[i].conscientiousnessCount +'</td><td>'+ Object.values(data.Result)[i].ExtraversionCount +'</td><td>'+ Object.values(data.Result)[i].AgreeablenessCount +'</td><td>'+ Object.values(data.Result)[i].NeuroticismCount +'</td><td>'+ Object.values(data.Result)[i].NeuroticismCount +'</td></tr>';
                // for(let j=0 ; j < data.Result[i].length; j++){

                // }
                $('#tblPersonalityPredicted').append(tableRow);
              }
            console.log(data.Result)
        },
    });
}


//#endregion    