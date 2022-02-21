$(document).ready(function() {
    $('#addSetBtn').click(function() {
        var name_set = prompt('Name of the set');
        if (name_set == null) {
            return;
        }
        console.log(name_set);
        postData({"set_name":name_set}, "/add-set", function(result) {
            var card = `
            <div class="col-8 col-lg-4 col-xl-3 d-flex align-self-stretch" style="width:auto;">
            <div class="card" data-id=`+ result.id + `>
                <div class="card-header text-center bg-dark text-white">
                    <div class="d-flex align-items-center">
                        <h5 class="mx-auto w-100">`+ result.name +`</h5>
                    </div>
                </div>
                <div class="card-body">
                    <a href="/set/`+ result.id +`/`+ result.name +`" class="card-link">Go to Set</a>
                    <button type="button" id="deleteSetBtn" class="btn btn-sm btn-danger">Delete Set</button>
                    <button type="button" id="updateSetBtn" class="btn btn-sm btn-info">Edit Name</button>
                </div>
            </div>
        </div>
            `
            $('#sets').append(card);
        })

    });

    $("body").on("click", "#deleteSetBtn", function(){
        console.log("clicked");
        var card = $(this).closest('.card');
        var set_id = card.data('id');
        postData({"set_id": set_id}, "/delete-set", function(result) {
            console.log(result);
            card.parent().remove();
        });
    });

    $("body").on("click", "#updateSetBtn", function() {
        console.log("clicked");
        var set = $(this).closest('.card');
        var title = set.find('h5');
        var set_id = set.data('id');
        var name_set = prompt('New Name of the set');
        if(name_set == null) {
            return;
        }
        postData({"set_id": set_id, "set_name": name_set}, "/update-set", function(result) {
            console.log(result);
            title.text(name_set);
        })
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