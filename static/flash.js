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
        postData({"question": question, "answer": answer, "path": path}, "/add-card",  function(result) {
            console.log(result.card_id);
            var html = `
            <div class="col-8 col-lg-4 col-xl-3 d-flex align-self-stretch">
            <button type="button" id="deleteBtn" class="btn-close btn-close-black" aria-label="Close"></button>
            <div class="flip-card mt-2" data-id=`+ result.card_id +`>
              <div class="flip-card-inner">
                <div class="flip-card-front">
                  <h2>`+ question +`</h2>
                </div>
                <div class="flip-card-back">
                  <h2>`+ answer +`</h2>
                </div>
              </div>
            </div>
          </div>  
            `
            $('#cards').append(html);
        }) 
        $('#exampleModal').modal('hide');
    });

    $("body").on("click", '.flip-card', function() {
        $(this).toggleClass('is-flipped');
    });

    $("body").on("click", '#deleteBtn', function() {
        console.log("clicked");
        var card_id = $(this).next().data('id');
        var card_div = $(this).parent()
        
        console.log(card_id);
        postData({"card_id": card_id}, "/delete-card", function(result) {
            console.log(result);
            card_div.remove();
        });
    });
});


function postData(send, link, callback) {
    $.ajax ({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: 'json',
        url: link,
        
    
    }).done(function(data){
        callback(data);
    });
}