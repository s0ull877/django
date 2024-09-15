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
    
    // удаляем отклик после клика
    notification_item = this.closest('.notification-item');
    notification_item.remove();

    // если откликов не осталосб, говорю об этом
    if  (!document.querySelector('.notification-item')) {
        no_notification = document.querySelector('.empty-notifications')
        no_notification.style.display = 'block'
    };

    // для дальнейшей обработки бек-ом
    if (this.classList.contains('approve-notification')) {
        // 
    } else {

    };
}

