const cart_object_info = new Map()
let card_list_item_list = document.getElementById('item_list');
const cart_objet = new Map()
const item_map = new Map()

function showAddToCartPopup(item_id) {
    const messageBox = document.getElementById("message");
    messageBox.innerHTML = ""; // Czyści zawartość
    messageBox.style.display = "block";

    const border = document.createElement('div')
    border.classList.add('styled-border-popup')
    const hide_button = document.createElement('div')
    const hide = document.createElement('button')
    hide.textContent = 'x';
    hide.addEventListener("click", () => {
        messageBox.innerHTML = "";
        messageBox.style.display = "none";
    });
    // Stwórz kontener popupu
    const popup = document.createElement("div");
    popup.classList.add('popup-class')

    // Zdjęcie
    const img = document.createElement("img");
    img.src = "data:image/jpeg;base64," + item_map.get(item_id).picture;
    img.alt = item_map.get(item_id).name;
    img.style.width = "100px";
    img.style.height = "100px";
    img.style.objectFit = "cover";
    img.style.marginBottom = "10px";

    // Informacje
    const name = document.createElement("h3");
    name.textContent = item_map.get(item_id).name;

    const stock = document.createElement("p");
    stock.textContent = "Dostępność: " + item_map.get(item_id).amount;

    const price = document.createElement("p");
    price.textContent = "Cena: " + item_map.get(item_id).price + " zł/szt";

    // Pole ilości
    const input = document.createElement("input");
    input.type = "number";
    input.min = "1";
    input.max = item_map.get(item_id).amount;
    input.value = "1";
    input.style.margin = "10px 0";
    input.style.width = "80%";

    // Przycisk dodaj
    const button = document.createElement("button");
    button.textContent = "Dodaj do koszyka";
    button.style.marginTop = "10px";
    button.style.padding = "8px 12px";
    button.style.cursor = "pointer";

    button.addEventListener("click", () => {
        const amountToAdd = parseInt(input.value);

        if (isNaN(amountToAdd) || amountToAdd < 1 || (cart_objet.get(item_id) + amountToAdd) > item_map.get(item_id).amount) {
            input.style.border = "2px solid red";
            return;
        }
        cart_objet.set(item_id, (cart_objet.get(item_id) || 0) + amountToAdd)
        cart_object_info.set(item_id, item_map.get(item_id))

        createCartItemCard(item_id)
        document.getElementById("cart-cost").innerText = calculateTotal() + " zł";
        document.getElementById('addAudio').currentTime = 0
        document.getElementById('addAudio').play()
        // Ukryj popup
        messageBox.innerHTML = "";
        messageBox.style.display = "none";
    });

    // Dodaj wszystko do popupu
    hide_button.appendChild(hide);
    border.appendChild(hide_button)


    popup.appendChild(img);
    popup.appendChild(name);
    popup.appendChild(stock);
    popup.appendChild(price);
    popup.appendChild(input);
    popup.appendChild(button);
    border.appendChild(popup)

    messageBox.appendChild(border)
    messageBox.style.display = "block";
}

function showRemoveFromCartPopup(item_id) {
    if (!cart_objet.get(item_id)) {
        return;
    }
    if (item_map.get(item_id)===undefined) return;
    const item = item_map.get(item_id);

    if (!item) {
        console.warn("Przedmiot nie istnieje w koszyku.");
        return;
    }

    const messageBox = document.getElementById("message");
    messageBox.innerHTML = "";
    const border = document.createElement('div')
    border.classList.add('styled-border-popup')
    const hide_button = document.createElement('div')
    const hide = document.createElement('button')
    hide.textContent = 'x';
    hide.addEventListener("click", () => {
        messageBox.innerHTML = "";
        messageBox.style.display = "none";
    });

    // Stwórz kontener popupu
    const popup = document.createElement("div");
    popup.classList.add('popup-class');

    // Zdjęcie
    const img = document.createElement("img");
    img.src = "data:image/jpeg;base64," + item.picture;
    img.alt = item.name;
    img.style.width = "100px";
    img.style.height = "100px";
    img.style.objectFit = "cover";
    img.style.marginBottom = "10px";

    const name = document.createElement("h3");
    name.textContent = item.name;

    const inCart = document.createElement("p");
    inCart.textContent = "W koszyku: " + item.amount;

    const price = document.createElement("p");
    price.textContent = "Cena: " + item.price + " zł/szt";

    const input = document.createElement("input");
    input.type = "number";
    input.min = "1";
    input.max = item.amount;
    input.value = "1";
    input.style.margin = "10px 0";
    input.style.width = "80%";

    const button = document.createElement("button");
    button.textContent = "Usuń z koszyka";
    button.style.marginTop = "10px";
    button.style.padding = "8px 12px";
    button.style.cursor = "pointer";

    button.addEventListener("click", () => {
        const toRemove = parseInt(input.value);
        if (isNaN(toRemove) || toRemove < 1 || toRemove > item.amount) {
            input.style.border = "2px solid red";
            return;
        }

        if (toRemove >= cart_objet.get(item_id)) {
            const card = document.getElementById(`cart-item-${item_id}`);
            if (card) card.remove();
            cart_objet.delete(item_id)
            cart_object_info.delete(item_id)

            createCartItemCard(item_id)

        } else {
            cart_objet.set(item_id, (cart_objet.get(item_id) - toRemove))
            createCartItemCard(item_id)
        }
        document.getElementById('removeAudio').currentTime = 0
        document.getElementById('removeAudio').play()
        sessionStorage.setItem("cart", JSON.stringify(cart_objet));
        document.getElementById("cart-cost").innerText = calculateTotal() + " zł";

        messageBox.innerHTML = "";
        messageBox.style.display = "none";
    });

    hide_button.appendChild(hide);
    border.appendChild(hide_button)


    popup.appendChild(img);
    popup.appendChild(name);
    popup.appendChild(price);
    popup.appendChild(input);
    popup.appendChild(button);
    border.appendChild(popup)

    messageBox.appendChild(border)
    messageBox.style.display = "block";
}

window.addEventListener("DOMContentLoaded", () => {
    loadCartFromSession();
});

function loadCartFromSession() {
    const json = sessionStorage.getItem("sessionCart");
    if (!json) {
        // pusta mapa, jeśli nic nie ma
    }
    // Parsujemy do tablicy
    const entries = JSON.parse(json);
    // Odtwarzamy Mapę
    let temp = new Map(entries);
    let id_list = [];
    temp.forEach((value, key) => {
        cart_objet.set(key, value);
        id_list.push(key);
    })
    getCartItemFromDB(id_list);
    cart_objet.forEach((value, key, map) => {
        createCartItemCard(key)

    })
    // Zaktualizuj całkowity koszt
    const total = calculateTotal();
    document.getElementById("cart-cost").innerText = total + " PLN";
}

function saveCartToSession() {
    const entries = Array.from(cart_objet.entries());
    // Serializujemy
    const json = JSON.stringify(entries);
    // Zapisujemy
    sessionStorage.setItem("sessionCart", json);
}

function getCartItemFromDB(list_of_id) {

    fetch('sessionCartItemInfo', {
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            ids: [...list_of_id]
        }),
    }).then(response => {
        if (!response.ok) throw new Error("Błąd sieci!");
        return response.json();
    }).then(data => {
        console.log("Odpowiedź serwera:", data['received']);
        if (data['received']) {
            console.log('empty')
        }
        let items = JSON.parse(data['received'])
        items.forEach(item => {
            console.log(item)
            cart_object_info.set(item['id'], item);
            item_map.set(item['id'], item)
        })
        cart_objet.forEach((value, key, map) => {
                console.log("here is map of item")
                console.log(item_map)
                console.log(cart_object_info)
                createCartItemCard(key);
            }
        )
    }).catch(error => {
        console.error("Wystąpił błąd:", error);
    })


}

function createCartItemCard(item_id) {
    console.log('item sent to create cart function')
    console.log(item_id)
    console.log(cart_objet.get(item_id))
    console.log(cart_objet)
    if (cart_objet.get(item_id) === undefined) {
        return;
    }
    let card = document.createElement('div');
    if (document.getElementById(`cart-item-${item_id}`)) {
        console.log('div found');
        card = document.getElementById(`cart-item-${item_id}`);
        card.innerHTML = '';
    } else {
        console.log('created new div');
        card = document.createElement('div');
        card.classList.add("mini-item-card");
        card.id = `cart-item-${item_id}`;
    }


    const img = document.createElement("img");
    img.src = "data:image/jpeg;base64," + item_map.get(item_id).img;
    img.alt = item_map.get(item_id).name;
    img.classList.add("mini-item-img");
    card.appendChild(img);

    const name = document.createElement("p");
    name.classList.add("mini-item-name");
    name.textContent = item_map.get(item_id).name;
    card.appendChild(name);

    const details = document.createElement("p");
    details.classList.add("mini-item-details");
    details.textContent = `x${cart_objet.get(item_id)} | ${item_map.get(item_id).price} zł/szt`;
    card.appendChild(details);

    const removeBtn = document.createElement("button");
    removeBtn.textContent = "Usuń";
    removeBtn.classList.add("remove-button");
    removeBtn.addEventListener("click", () => {
        showRemoveFromCartPopup(item_id);
    });
    card.appendChild(removeBtn);
    document.getElementById("cart-items").appendChild(card);

    const total = calculateTotal();
    document.getElementById("cart-cost").innerText = total + " PLN";
}

function calculateTotal() {
    console.log('calculate price')
    let total = 0;
    cart_objet.forEach((value, key, mapInstance) => {
        total += value * item_map.get(key).price
    });

    saveCartToSession();
    animated_cart();
    return total.toFixed(2);
}

function clearCart() {
    sessionStorage.removeItem("cart");
    sessionStorage.clear();
    document.getElementById("cart-items").innerHTML = "";
    document.getElementById("cart-cost").innerText = "0.00";
    document.getElementById('removeAudio').currentTime = 0;
    document.getElementById('removeAudio').play();
    animated_cart();
    cart_objet.clear();
}