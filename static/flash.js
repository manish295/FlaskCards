$(document).ready(function() {
    $('#addCardBtn').click(function () {
        console.log("modal on");
        $('#exampleModal').modal('show');
    });

    $('#closeModal').click(function() {
        console.log("modal off");
        $('#questionField').val('');
        $('#answerField').val('');
        $('#exampleModal').modal('hide');
    });

    $('#saveChanges').click(function() {
        console.log("modal off");
        var question = $('#questionField').val();
        var answer = $('#answerField').val();
        var path = window.location.pathname;
        if (question == "" || answer == "") {
            alert("Please fill out the fields!");
            return;
        }
        $('#questionField').val('');
        $('#answerField').val('');
        postData({"question": question, "answer": answer, "path": path}, function(result) {
            console.log(result);
            var html = `
            <div class="col-8 col-lg-4 col-xl-3 d-flex align-self-stretch">
                <div class="flip-card mt-2">
                <div class="flip-card-inner">
                    <div class="flip-card-front">
                    <h2>`+ question +`</h2>
                    </div>
                    <div class="flip-card-back">
                    <h2>`+ answer + `</h2>
                    </div>
                </div>
                </div>
            </div>`
            document.getElementById('cards').insertAdjacentHTML('beforeend', html);
        }) 
        $('#exampleModal').modal('hide');
    });

    $("body").on("click", '.flip-card', function() {
        $(this).toggleClass('is-flipped');
    });

});


function postData(send, callback) {
    $.ajax ({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: 'json',
        url: "/add-card",
        
    
    }).done(function(data){
        callback(data);
    });
}