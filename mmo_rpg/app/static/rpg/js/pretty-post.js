function prettyPost(media_div) {

    items = media_div.querySelectorAll('.media-item');

    switch (items.length) {
        case 1:
            
            image = media_div.querySelector('img');
            image.style.maxHeight = '380px';
            media_div.style.display = 'flex';
            media_div.style.justifyContent = 'center';
            break;

        case 2:

            media_div.style.display = 'flex';
            media_div.style.justifyContent = 'center';


            last_image = media_div.querySelectorAll('img')[1];

            first_image = media_div.querySelectorAll('img')[0];
            first_image.style.position = 'flex';

            if (first_image.height > last_image.height) {
                
                media_item = first_image.closest('.media-item');
                media_item.style.height = `${last_image.height}px`;

            } else {

                media_item = last_image.closest('.media-item');
                media_item.style.height = `${first_image.height}px`;
                
            }

            break;

        case 3:

            images = media_div.querySelectorAll('img');
            media_items = media_div.querySelectorAll('.media-item');

            if (images[0].height > images[1].height) {

                media_div.style.gridTemplateColumns = 'repeat(2, 1fr)';
                media_div.style.gridTemplateRows = 'repeat(2, 1fr)';
                media_items[0].style.gridArea = '1 / 1 / 3 / 2'
                media_items[1].style.gridArea = '1 / 2 / 2 / 3'
                media_items[2].style.gridArea = '2 / 2 / 3 / 3'
                
                media_div.style.maxHeight = `${images[0].height}px`;
                
            } else {

                media_div.style.gridTemplateColumns = 'repeat(2, 1fr)';
                media_div.style.gridTemplateRows = 'repeat(2, 1fr)';
                media_items[0].style.gridArea = '1 / 1 / 2 / 3'
                media_items[1].style.gridArea = '2 / 1 / 3 / 2'
                media_items[2].style.gridArea = '2 / 2 / 3 / 3'
                
                if (images[1].height > images[2].height) {

                    media_div.style.maxHeight = `${images[0].height + 10 + images[2].height}px`;


                } else {

                    media_div.style.maxHeight = `${images[0].height + 10 + images[1].height}px`;

                }

            }

            break;

    }

}

let media_divs = document.querySelectorAll('.media-post-data');

media_divs.forEach((media_div) =>{
    
    prettyPost(media_div)

})

