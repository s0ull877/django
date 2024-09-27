// кнопка удаления 
let notification_buttons = document.querySelectorAll('.delete-notification-btn')

// вешаем хендлер на кнопки
notification_buttons.forEach((button) => {
    button.addEventListener('click', deleteComment); 
})



function deleteComment() {
    
    var notification_id = $(this).attr('notification_id')
    var token = this.querySelector('input[name="csrfmiddlewaretoken"]').value;

    
    
    $.ajax({
        type: "POST",
        url: $(this).attr('change_url'),
        data: {
            notification_id: notification_id,
            post_owner: $(this).attr('post_owner'),
            notf_owner: $(this).attr('notification_owner'),
            csrfmiddlewaretoken: token,
        },
        success: function (data) {

            var notification_block = document.querySelector(`#notification-${data.pk}`);

            notification_block.remove(notification_block);

        },
        error: function(data){
            console.log(data.responseJSON.error);
        }
    })

}
