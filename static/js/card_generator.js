// front page card gen.
function generate_item_card(item) {
    const info_section = document.createElement('div');
    info_section.classList.add('info-section');

    const top_info = document.createElement('div');
    top_info.classList.add('top-info');


    const sub_top_info = document.createElement('div');
    sub_top_info.classList.add('sub-top-info');

    const button_info = document.createElement('div');
    button_info.classList.add('button_info');

    const styled_border = document.createElement('div');
    styled_border.classList.add('styled-border');
    styled_border.classList.add('wave-background');

    const card = document.createElement('div');
    card.classList.add('card');

    const new_img = document.createElement('img');
    new_img.classList.add('item-pic');
    new_img.src = "data:image/jpeg;base64," + item.picture;
    new_img.alt = item.name;

    const nameEl = document.createElement('h2');
    nameEl.classList.add('item_name');
    nameEl.textContent = item.name;

    function createInfoRow(label, value) {
        const row = document.createElement('p');
        row.classList.add('par');
        if (label === 'price') {
            row.innerHTML = `<strong>${label}:</strong> ${value} PLN`;
        } else {
            row.innerHTML = `<strong>${label}:</strong> ${value}`;
        }
        return row;
    }

    const button = document.createElement('button');
    button.id = 'button' + item.id;
    button.className = 'action-button';
    button.textContent = 'Kup teraz';

    button.addEventListener('click', () => {
        button.addEventListener('click', () => {
            showAddToCartPopup(item.id);
        });
    });


    styled_border.appendChild(card);
    card.appendChild(new_img);
    card.appendChild(info_section);
    info_section.appendChild(top_info);
    info_section.appendChild(sub_top_info);
    info_section.appendChild(button_info);

    button_info.appendChild(createInfoRow('Typ', item.type));
    button_info.appendChild(createInfoRow('source', item.work_source));
    button_info.appendChild(createInfoRow('genre', item.type));
    button_info.appendChild(createInfoRow('tags', item.tags));
    button_info.appendChild(createInfoRow('feature', item.feature));
    button_info.appendChild(createInfoRow('drop data', item.drop_data));
    button_info.appendChild(createInfoRow('renewable', item.renewable));

    top_info.appendChild(nameEl);
    sub_top_info.appendChild(createInfoRow('price', item.price));
    sub_top_info.appendChild(createInfoRow('amount', item.amount));
    info_section.appendChild(button);

    return styled_border;
}

//list page card gen
function generate_card(item) {

        item_map.set(item.id, item)
        const info_section = document.createElement('div');
        info_section.classList.add('info-section');

        const top_info = document.createElement('div');
        top_info.classList.add('top-info');


        const button_info = document.createElement('div');
        button_info.classList.add('button_info');


        const sub_top_info = document.createElement('div');
        sub_top_info.classList.add('sub-top-info');

        const styled_border = document.createElement('div');
        styled_border.classList.add('styled-border');
        styled_border.classList.add('wave-background');

        const card = document.createElement('div');
        card.classList.add('card');

        const new_img = document.createElement('img');
        new_img.classList.add('item-pic');
        new_img.src = "data:image/jpeg;base64," + item.picture;
        new_img.alt = item.name;

        const nameEl = document.createElement('h2');
        nameEl.classList.add('item_name');
        nameEl.textContent = item.name;

        function createInfoRow(label, value) {
            const row = document.createElement('p');
            row.classList.add('par');
            if (label === 'price') {
                row.innerHTML = `<strong>${label}:</strong> ${value} PLN`;
            } else {
                row.innerHTML = `<strong>${label}:</strong> ${value}`;
            }
            return row;
        }

        const button = document.createElement('button');
        button.id = 'button' + item.id;
        button.className = 'action-button';
        button.textContent = 'Kup teraz';

        button.addEventListener('click', () => {
            button.addEventListener('click', () => {
                showAddToCartPopup(item.id);
            });
        });


        styled_border.appendChild(card);
        card.appendChild(new_img);
        card.appendChild(info_section);
        info_section.appendChild(top_info);
        info_section.appendChild(sub_top_info);
        info_section.appendChild(button_info);

        button_info.appendChild(createInfoRow('Typ', item.type));
        button_info.appendChild(createInfoRow('source', item.work_source));
        button_info.appendChild(createInfoRow('genre', item.type));
        button_info.appendChild(createInfoRow('tags', item.tags));
        button_info.appendChild(createInfoRow('feature', item.feature));
        button_info.appendChild(createInfoRow('drop data', item.drop_data));
        button_info.appendChild(createInfoRow('renewable', item.renewable));

        top_info.appendChild(nameEl);
        sub_top_info.appendChild(createInfoRow('price', item.price));
        sub_top_info.appendChild(createInfoRow('amount', item.amount));
        info_section.appendChild(button);

        return  styled_border;
}