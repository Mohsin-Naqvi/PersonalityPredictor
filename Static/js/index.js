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
    $("#tblPersonalityPredicted").find("tr:gt(0)").remove();

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
                var tableRow = '<tr><td>' + Object.values(data.Result)[i].resumeID + '</td><td>' + Object.values(data.Result)[i].opennessCount + '</td><td>'+ Object.values(data.Result)[i].conscientiousnessCount +'</td><td>'+ Object.values(data.Result)[i].ExtraversionCount +'</td><td>'+ Object.values(data.Result)[i].AgreeablenessCount +'</td><td>'+ Object.values(data.Result)[i].NeuroticismCount +'</td><td>'+ Object.values(data.Result)[i].PredictedPeronsalityName  +'</td></tr>';
                
                $('#tblPersonalityPredicted').append(tableRow);
              }
            console.log(data.Result)
        },
    });
}

function GetPredictPersonalityByResumeHandler(){
    $.ajax({
      type: "POST",
      url: "/predict_personality_by_resume",
      dataType: 'JSON',
      // data: {
      //     userJD: userJD
      // },
      success: function (data) {               
          console.log(data)
      },
  });
}
//#endregion    