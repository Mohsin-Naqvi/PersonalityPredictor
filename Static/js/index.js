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
  $("#btnPredictPersonalityByResumeHandler").click(GetPredictPersonalityByResumeHandler);
  return false;
});

//#endregion

//#region Prediction 

function GetPredictPersonalityHandler() {
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
        var tableRow = '<tr><td>' + Object.values(data.Result)[i].resumeID + '</td><td>' + Object.values(data.Result)[i].opennessCount + '</td><td>' + Object.values(data.Result)[i].conscientiousnessCount + '</td><td>' + Object.values(data.Result)[i].ExtraversionCount + '</td><td>' + Object.values(data.Result)[i].AgreeablenessCount + '</td><td>' + Object.values(data.Result)[i].NeuroticismCount + '</td><td>' + Object.values(data.Result)[i].PredictedPeronsalityName + '</td></tr>';

        $('#tblPersonalityPredicted').append(tableRow);
      }
      console.log(data.Result)
    },
  });
}

function GetPredictPersonalityByResumeHandler() {
  debugger;
  let userJD = document.getElementById('txtJobDescription').value
  $("#tblPersonalityPredicted").find("tr:gt(0)").remove();
  let CSRF = getCSRFCookie();

  var form_data = new FormData();
  var ins = document.getElementById('resumeFile').files.length;

  if (ins == 0) {
    $('#msg').html('<span style="color:red">Select at least one file</span>');
    return;
  }

  for (var x = 0; x < ins; x++) {
    form_data.append("files[]", document.getElementById('resumeFile').files[x]);
  }

  csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

  //console.log(csrf_token);
  form_data.append("userJD",userJD);
  form_data.append("csrfmiddlewaretoken", csrf_token);

  $.ajax({
    url: '/predict_personality_by_resume', // point to server-side URL
    dataType: 'json', // what to expect back from server
    cache: false,
    contentType: false,
    processData: false,
    data: form_data,
    type: 'POST',
    success: function (data) { // display success response      
      for (let i = 0; i < Object.keys(data.Result).length; i++) {
        var tableRow = '<tr><td>' + Object.values(data.Result)[i].resumeID + '</td><td>' + Object.values(data.Result)[i].opennessCount + '</td><td>' + Object.values(data.Result)[i].conscientiousnessCount + '</td><td>' + Object.values(data.Result)[i].ExtraversionCount + '</td><td>' + Object.values(data.Result)[i].AgreeablenessCount + '</td><td>' + Object.values(data.Result)[i].NeuroticismCount + '</td><td>' + Object.values(data.Result)[i].PredictedPeronsalityName + '</td></tr>';

        $('#tblPersonalityPredicted').append(tableRow);
      }
    }
  });

  // let formData = new FormData();           
  // formData.append("file", fileupload.files[0]);
  // console.log(formData)
  //   $.ajax({
  //     type: "POST",
  //     url: "/predict_personality_by_resume",
  //     dataType: 'JSON',
  //     processData: false,
  //     data: {
  //       csrfmiddlewaretoken: CSRF,
  //       file: formData
  //     },
  //     success: function (data) {               
  //         console.log(data)
  //     },
  // });
}

//#endregion    

//#region Helper Methods

function getCSRFCookie() {
  c_name = 'csrftoken';

  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}

 //#endregion