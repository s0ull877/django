// если нет откликов сразу показываем
if  (!document.querySelector('.notification-item')) {
    no_notification = document.querySelector('.empty-notifications')
    no_notification.style.display = 'block'
};


// кнопки принятия\отказа для отклика
let notification_buttons_divs = document.querySelectorAll('.notification-buttons')

// вещаем хендлер на кнопки
notification_buttons_divs.forEach((notification_buttons_div) => {
    notification_buttons_div.childNodes[1].addEventListener('click', deleteNotification); //approve
    notification_buttons_div.childNodes[3].addEventListener('click', deleteNotification); //eject
})



function deleteNotification() {
    // блок отклика
    var notification_item = this.closest('.notification-item');

    // данные для запроса
    var token = this.querySelector('input[name="csrfmiddlewaretoken"]').value

    // для дальнейшей обработки бек-ом
    if (this.classList.contains('approve-notification')) {
        var value = true
    } else {
        var value = false
    };
    
    $.ajax({
        type: "POST",
        url: $(this).attr('change_url'),
        data: {
            notification_id: $(this).attr('notification_id'),
            value: value,
            csrfmiddlewaretoken: token,
        },
        success: function (data) {

            // удаляем отклик после ответа
            console.log(notification_item)
            notification_item.remove();

            // если откликов не осталосб, говорю об этом
            if  (!document.querySelector('.notification-item')) {
                var no_notification = document.querySelector('.empty-notifications')
                no_notification.style.display = 'block'
            };
        },
        error: function(data){
            console.log(data.responseJSON.error);
        }
    })

}

