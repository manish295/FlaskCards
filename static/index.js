$(document).ready(function() {
    $('#addSetBtn').click(function() {
        var name_set = prompt('Name of the set');
        console.log(name_set);
        postData({"set_name":name_set}, function(result) {
            var card = `
            <div class="col-8 col-lg-4 col-xl-3 d-flex align-self-stretch">
                <div class="card" style="width: 18rem;">
                    <div class="card-body">
                        <h5 class="card-title">`+ result.name +`</h5>
                        <a href="/set/`+ result.id +`" class="card-link">Go to Set</a>
                    </div>
                </div>
            </div>
            `
            document.getElementById('sets').insertAdjacentHTML('beforeend', card);
        })

    });
});

function postData(send, callback) {
    $.ajax ({
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(send),
        dataType: 'json',
        url: "/add-set",
        
    
    }).done(function(data){
        callback(data);
    });
}