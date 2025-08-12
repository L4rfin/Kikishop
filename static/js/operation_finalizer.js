let total_price = 0;
document.getElementById('checkout-button').addEventListener('mousedown', (e) => {
    const form = document.getElementById("checkout-form");
    const formData = new FormData(form);
    const data = {
        name: formData.get("name"),
        street: formData.get("street"),
        building_number: formData.get("building_number"),
        local_number: formData.get("local_number"),
        local_letter: formData.get("local_letter"),
        post_code_2: formData.get("post_code_2"),
        post_code_3: formData.get("post_code_3"),
        city: formData.get("city"),
        cuntry: formData.get("cuntry"),
        contact: document.getElementById('communication-option').value,
        contact_address: formData.get("contact_address")
    };
    console.log(data)
    // check if all user input is provided and cart is not empty

    if (checkSentData(data)) {
        //check if selected email and provided valid email address
        if (data.contact === 'Email' && emailValidator(data.contact_address)) {
            show_finalization_popup(data)
        }
        //wrong email address provided handler
        if (data.contact === 'Email' && !emailValidator(data.contact_address)) {
            wrongEmailResponder()
        }

        //check if selected any of social media and provided valid url address
        if ((data.contact === 'Instagram') && linkValidator(data.contact_address, data.contact)) {
            show_finalization_popup(data)
        }

        //wrong url address provided handler
        if ((data.contact === 'Instagram') && !linkValidator(data.contact_address, data.contact)) {
        }

    }

});

function setSelectionInput() {
    if (document.getElementById('input-for-communication-address')) {
        document.getElementById('label-for-communication-method').innerHTML = '';
    }
    let option = document.getElementById('communication-option');
    let labl = document.getElementById('label-for-communication-method');
    let input = document.createElement('input');
    input.name = 'contact_address'
    input.id = 'input-for-communication-address'
    console.log(option.value)
    switch (option.value) {
        case 'Email': {
            input.type = "email";
            labl.innerText = 'wprowadź email kontaktowy';
            labl.appendChild(input);
        }
            break;
        case 'Instagram': {
            input.type = "text";
            labl.innerText = 'podaj lik do profilu, pamiętaj by profil był publiczny';
            labl.appendChild(input);
        }
            break;
        default: {
            input.innerHTML = ''
            labl.innerText = '';
        }
            break;
    }
}

function checkSentData(data) {
    if (data.name === '') {
        console.log('1')
        return false
    }
    if (data.street === '') {
        console.log('12')
        return false
    }
    if (data.building_number === '') {
        console.log('13')
        return false
    }
    if (data.post_code_2 === '') {
        console.log('14')
        return false
    }
    if (data.post_code_3 === '') {
        console.log('15')
        return false
    }
    if (data.location === '') {
        console.log('16')
        return false
    }
    if (data.cuntry === '') {
        console.log('17')
        return false
    }
    if (data.contact === '') {
        console.log('18')
        return false
    }
    if (data.contact_address === '') {
        console.log('19')
        return false
    }
    return true;
}

function show_finalization_popup(data_info) {
    console.log('show fin')
    const messageBox = document.getElementById("message");
    messageBox.innerHTML = ""; // Czyści zawartość
    messageBox.style.display = "block";

    const border = document.createElement('div')
    border.classList.add('styled-border-popup')
    const hide_button = document.createElement('div')
    const hide = document.createElement('button')
    hide.style.margin = "5px"
    hide.textContent = 'x';
    hide.addEventListener("click", () => {
        messageBox.innerHTML = "";
        messageBox.style.display = "none";
    });
    // Stwórz kontener popupu
    const popup = document.createElement("div");
    popup.classList.add('popup-class')
    const item_list = document.createElement('div');
    const message = document.createElement('div');
    const h1 = document.createElement('h1');
    h1.innerText = 'here gonna be finalization of ordering and trusted payment procedure';
    const h2 = document.createElement('h2');
    h2.innerText = 'but dou to structural of my business activity (Unregistered activity)'
    const gov_link = document.createElement("a");
    gov_link.href = 'https://www.biznes.gov.pl/pl/portal/00115'
    gov_link.text = 'Unregistered_activity.gov.pl'

    const message_template_div = document.createElement('div');
    const message_template = document.createElement('textarea');
    generateTransactionTemplate(message_template, data_info)
    const button_confirm = document.createElement("button");
    button_confirm.innerText = 'confirm'
    button_confirm.addEventListener("click", () => {
        sendOrder(data_info)
    })


    message_template_div.appendChild(message_template)
    message_template_div.appendChild(button_confirm)

    message.appendChild(h1)
    message.appendChild(h2)
    message.appendChild(gov_link)
    message.appendChild(message_template_div)
    popup.appendChild(item_list)
    popup.appendChild(message)


    // Dodaj wszystko do popupu
    hide_button.appendChild(hide);
    border.appendChild(hide_button)
    border.appendChild(popup)

    messageBox.appendChild(border)
    messageBox.style.display = "block";
}

function generateTransactionTemplate(textarea, info_data) {
    let letter_address = info_data.street + ' ' + info_data.building_number;
    if (info_data.local_number !== '') letter_address += '/' + info_data.local_number
    if (info_data.local_letter !== '') letter_address += info_data.local_letter + "\n"
    letter_address += info_data.post_code_2 + '-'
    letter_address += info_data.post_code_3 + "\n"
    letter_address += info_data.location + " "
    letter_address += info_data.cuntry
    let text = '';
    let contact_info = 'name: ' + info_data.name + "\n" + "address: " + letter_address + '\n' + "contact form: " + info_data.contact + '\n' + "contact" + info_data.contact + '' + info_data.contact_address + '\n' + '\n';
    textarea.textContent += contact_info;
    cart_objet.forEach((value, key) => {
            textarea.textContent += '{'
            text = 'id:' + key + ', name:' + cart_object_info.get(key).name + ", amount:" + value + ", price:" + (cart_object_info.get(key).price * value)
            textarea.textContent += text + '}';
            total_price += (cart_object_info.get(key).price * value)
        }
    )
    textarea.textContent += "total: " + total_price;

    return text;
}

function emailValidator(email) {
    return String(email)
        .toLowerCase()
        .match(
            /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        );
}

function linkValidator(url, method) {
    if (url.concat('instagram.com') && method === 'Instagram') {

        try {
            const parsed = new URL(url);
            return parsed.hostname === "www.instagram.com" && parsed.pathname.split("/")[1] !== "";
        } catch (e) {
            return false;
        }
    }

    // not finish function for validated messenger or facebook url

    // if (url.concat('m.me') || url.concat('messenger.com') && method === 'Messenger') {
    //
    //     try {
    //         const parsed = new URL(url);
    //         const hostname = parsed.hostname;
    //         return (
    //             (hostname === "m.me" && parsed.pathname.split("/")[1] !== "") ||
    //             (hostname === "www.messenger.com" && parsed.pathname.startsWith("/t/"))
    //         );
    //     } catch (e) {
    //         return false;
    //     }
    // }
}

function wrongEmailResponder() {
    document.getElementById('input-for-communication-address').style.background = "red"

}

function sendOrder(data_info) {
    let items_ids = ''
    let items_value = ''

    cart_objet.forEach((value, key) =>{
        items_ids += key + ','
        items_value += value + ','
    })
    fetch('orderSender', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: data_info.name,
            items: items_ids,
            items_amount: items_value,
            price: total_price,
            city: data_info.city,
            street: data_info.street,
            postal_code: data_info.post_code_2 + '-' + data_info.post_code_3,
            location: data_info.location,
            cuntry: data_info.cuntry,
            building_number: data_info.building_number + '/' + data_info.local_number + data_info.local_letter,
            contact_address: data_info.contact_address,
        }),
    }).then(response => {
        if (!response.ok) throw new Error("Błąd sieci!");
        return response.json();
    }).then(data => {
        console.log("Odpowiedź serwera:", data['received']);
        if (data['received'] > 0) {
            orderInfoPopup(data['received'])
            cart_objet.clear()
            clearCart()
        }
    }).catch(error => {
        console.error("Wystąpił błąd:", error);
    })
}

function orderInfoPopup(order_id) {
    const messageBox = document.getElementById("message");
    messageBox.innerHTML = ""; // Czyści zawartość
    messageBox.style.display = "block";
    const border = document.createElement('div')
    border.classList.add('styled-border-popup')
    const hide_button = document.createElement('div')
    const hide = document.createElement('button')
    hide.style.margin = "5px"
    hide.textContent = 'x';
    hide.addEventListener("click", () => {
        messageBox.innerHTML = "";
        messageBox.style.display = "none";
    });

    const h1 = document.createElement('h1');
    h1.textContent = "thank you for order";

    const h2 = document.createElement('h2');
    h2.textContent = "here is bank account address: \n or \n phone address for blick: ";

    const div = document.createElement('div');

    const p = document.createElement('p');
    p.textContent = "thank you for trust and support \n your small artist";

    const img = document.createElement('img');
    img.src = '/static/images/smallKiki.webp';
    img.alt = 'thank you';
    img.style.width = "50%"

    // Składanie struktury
    div.appendChild(p);
    div.appendChild(img);
    hide_button.appendChild(hide);
    border.appendChild(hide_button)


    // Stworzenie kontenera i dodanie wszystkiego do niego
    const container = document.createElement('div');
    container.classList.add('popup-class')
    container.appendChild(h1);
    container.appendChild(h2);
    container.appendChild(div);
    border.appendChild(container)
    messageBox.appendChild(border)
}