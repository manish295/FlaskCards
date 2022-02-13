$(document).ready(function() {
    $('#addSetBtn').click(function() {
        var name_set = prompt('Name of the set');
        if (name_set == null) {
            return;
        }
        console.log(name_set);
        postData({"set_name":name_set}, "/add-set", function(result) {
            var card = `
            <div class="col-8 col-lg-4 col-xl-3 d-flex align-self-stretch">
                <div class="card" style="width: 18rem;">
                    <div class="card-body">
                        <h5 class="card-title">`+ result.name +`</h5>
                        <a href="/set/`+ result.id +`/`+ result.name +`" class="card-link">Go to Set</a>
                        <button type="button" id="deleteSetBtn" class="btn btn-danger">Delete Set</button>
                    </div>
                </div>
            </div>
            `
            document.getElementById('sets').insertAdjacentHTML('beforeend', card);
        })

    });

    $("body").on("click", "#deleteSetBtn", function(){
        console.log("clicked");
        var href = $(this).closest('.card-body').find('a').attr('href')
        var set_id = href.substr(5)
        console.log(set_id);
        set_id = set_id.substr(0, set_id.indexOf("/"))
        console.log(set_id);
        var div = $(this).closest('.card').parent();
        postData({"set_id": set_id}, "/delete-set", function(result) {
            console.log(result);
            div.remove();
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