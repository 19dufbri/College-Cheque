let  numColleges = 1;

$(function(ready) {

    function getCookie(c_name) {
        if (document.cookie.length>0) {
          c_start=document.cookie.indexOf(c_name + "=");
          if (c_start!=-1)
            {
            c_start=c_start + c_name.length+1;
            c_end=document.cookie.indexOf(";",c_start);
            if (c_end==-1) c_end=document.cookie.length;
            return document.cookie.substring(c_start,c_end);
            }
        } else {
            $(".progress-bar").css('width', '0%');
        }
        $(".progress-bar").css('width', '0%');
        return "";
    }

    if (getCookie("college-input-data") != "") {
        let cookie = getCookie("college-input-data");

        let parsedCookie = JSON.parse(cookie);

        $('#sex').val(parsedCookie.sex);
        $('#race').val(parsedCookie.race);
        $('#state').val(parsedCookie.state);
        $('#income').val(parsedCookie.income);
        $('#dependent').val(parsedCookie.dependent);
        $('#pell').val(parsedCookie.pell);
        $('#1stGen').val(parsedCookie.firstGen);
        $('#degree').val(parsedCookie.degree);
        $('#collegeName1').val(parsedCookie.collegeNames[0]);
        for(let i = 1; i < parsedCookie.collegeNames.length; i++) {
            //$("#collegeInputs").append('<input type="text" class="form-control collegeName" id="collegeName' + (i+1) + '" aria-describedby="collegeName" placeholder="Enter college name">')
            $('#collegeName' + (i+1)).val(parsedCookie.collegeNames[i]);
            $('#collegeName' + (i+1)).css("display","inline-block");
        }
        numColleges = parsedCookie.collegeNames.length;
        if(numColleges > 1) {
            $('#remBtn').css('display', 'inline-block');
        }
    } else {
        $("#progBar").css('width', '0%');

    }


    $('#nextBtn1').on('click', function (e) {
         $(".progress-bar").css('width', '25%');
    })

    $('#nextBtn2').on('click', function (e) {
         $(".progress-bar").css('width', '50%');
    })

    $('#nextBtn3').on('click', function (e) {
         $(".progress-bar").css('width', '75%');
         updateBtnSubmit();
    })

    $('#backBtn2').on('click', function (e) {
         $(".progress-bar").css('width', '0%');
    })

    $('#backBtn3').on('click', function (e) {
         $(".progress-bar").css('width', '25%');
    })

    $('#backBtn4').on('click', function (e) {
         $(".progress-bar").css('width', '50%');
    })

    $('#addBtn').on('click', function (e) {
        numColleges++;
        //$("#collegeInputs").append('<input type="text" class="form-control collegeName" id="collegeName' + numColleges + '" aria-describedby="collegeName" placeholder="Enter college name">')
        $("#collegeName" + numColleges).css("display","inline-block");
        $('#submitBtn').addClass("disabled");
        if(numColleges > 1 && numColleges < 10) {
            $('#remBtn').css('display', 'inline-block');
        } else if(numColleges >= 10) {
            $('#addBtn').css('display', 'none');
        }
        updateBtnSubmit();
        $("#progBar").addClass("progress-bar-animated").delay(600).removeClass("progress-bar-animated");
    })

    $('#remBtn').on('click', function (e) {
        //$("#collegeName" + numColleges).remove();
        $("#collegeName" + numColleges).css("display","none");
        numColleges--;
        if(numColleges == 1) {
            $('#remBtn').css('display', 'none');
        } else {
            $('#addBtn').css('display', 'inline-block');
        }
        updateBtnSubmit();
    })

    $('#submitBtn').on('click', function (e) {
        let sex = $('#sex').val();
        let race = $('#race').val();
        let state = $('#state').val();
        let income = $('#income').val();
        let dependent = $('#dependent').val();
        let pell = $('#pell').val();
        let firstGen = $('#1stGen').val();
        let degree = $('#degree').val();
        let collegeNames = [numColleges];
        for(let i = 0; i < numColleges; i++) {
            collegeNames[i] = $("#collegeName" + (i+1)).val();
        }
        let jsonObj = {
            "sex": sex, // "male"/"female"
            "race": race, // "
            "state": state,
            "income": income,
            "dependent": dependent,
            "pell": pell,
            "firstGen": firstGen,
            "degree": degree,
            "collegeNames": collegeNames,
        }
        setCookie("college-input-data",JSON.stringify(jsonObj),60);
    })

    function setCookie(c_name,value,expireminutes) {
       var exdate=new Date();
       exdate.setMinutes(exdate.getMinutes()+expireminutes);
       document.cookie=c_name+ "=" + value +
       ((expireminutes==null) ? "" : ";expires="+exdate.toUTCString());
    }

    $('#nextBtn1').addClass("disabled");
    updateBtn1();
    function updateBtn1() {
        if (verify1()) {
            $('#nextBtn1').removeClass("disabled");
        } else {
            $('#nextBtn1').addClass("disabled");
        }
    }

    function verify1() {
        return ($('#sex').val() != '' && $('#race').val() != '' && $('#state').val() != '');
    }

    $('#sex').change(updateBtn1);
    $('#race').change(updateBtn1);
    $('#state').change(updateBtn1);


    $('#nextBtn2').addClass("disabled");
    updateBtn2();
    function updateBtn2() {
        if (verify2()) {
            $('#nextBtn2').removeClass("disabled");
        } else {
            $('#nextBtn2').addClass("disabled");
        }
    }

    function verify2() {
        return ($('#income').val() != '' && $('#dependent').val() != '' && $('#pell').val() != '');
    }

    $('#income').change(updateBtn2);
    $('#dependent').change(updateBtn2);
    $('#pell').change(updateBtn2);

    $('#nextBtn3').addClass("disabled");
    updateBtn3();
    function updateBtn3() {
        if (verify3()) {
            $('#nextBtn3').removeClass("disabled");
        } else {
            $('#nextBtn3').addClass("disabled");
        }
    }

    function verify3() {
        return ($('#1stGen').val() != '' && $('#degree').val() != '');
    }

    $('#1stGen').change(updateBtn3);
    $('#degree').change(updateBtn3);



    $('#submitBtn').addClass("disabled");
    if (getCookie("college-input-data") != "") {
        updateBtnSubmit();
    }

    updateBtnSubmit();

    function updateBtnSubmit() {
        if (verifySubmit()) {
            $('#submitBtn').removeClass("disabled");
            $(".progress-bar").css('width', '100%');
        } else {
            $('#submitBtn').addClass("disabled");
            $(".progress-bar").css('width', '75%');
        }
    }

    function verifySubmit() {
        let test = 1;
        for(let i = 0; i < numColleges; i++) {
            if(($('.collegeName').eq(i).val() == ''))
                test = 0;
        }
        return (test == 1)
    }

    $(document).on('input', '.collegeName', function(){
        updateBtnSubmit();
    });

    // Activate Carousel
    $("#myCarousel").carousel();

    // Enable Carousel Indicators
    $(".item").click(function(){
      $("#myCarousel").carousel(1);
    });

    // Enable Carousel Controls
    $(".left").click(function(){
      $("#myCarousel").carousel("prev");
    });

    if (getCookie("college-input-data") != "") {
        $(".progress-bar").css('width', '0%');
    }

});

