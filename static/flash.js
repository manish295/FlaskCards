$(document).ready(function() {
    $('#addCardBtn').click(function () {
        console.log("modal on");
        $('#exampleModal').modal('show');
    });

    $('#closeModal').click(function() {
        console.log("modal off");
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
        postData({"question": question, "answer": answer, "path": path}, function(result) {
            console.log(result);
            var html = `
                <li>Question: `+ result.question +` Answer: `+ result.answer +`</li>
            `
            $('#flashcards').append(html);
        }) 
        $('#exampleModal').modal('hide');
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