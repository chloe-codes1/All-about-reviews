$('#update').click(function(){
    const title = $('#review_title').text()
    const content = $('#review_content').text()
    const pk = $('#review_pk').text()
    $('#review_title').replaceWith("<input text='text' class='form-control d-inline' id='review_title' name='title' value='"+ title+ "'></input>")

    $('#review_content').replaceWith("<textarea text='text' class='form-control' id='review_content' rows='3' name='content'>"+content+ "</textarea>")

    $('#update').replaceWith("<input type='submit' class='btn btn-primary py-1 px-2 ml-2' id='update' value='Save'>")
    $('#delete').replaceWith("<button class='btn btn-secondary py-1 px-2 ml-2' id='cancel'><a class='text-white text-decoration-none' href='/community/review_detail/" + pk +"/'>Cancel</a></button>")
})

