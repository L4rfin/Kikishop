function animated_cart() {
    const div_cart = document.getElementById('cart-icon');
    div_cart.classList.remove('animate-cart-start');
    void div_cart.offsetWidth;
    div_cart.classList.add('animate-cart-start');
    div_cart.addEventListener('animationend', function handler() {
        div_cart.classList.remove('animate-cart-start');
        div_cart.removeEventListener('animationend', handler);
    });
}

document.getElementById('cart-icon').addEventListener('click', () => {
    let cartPanel = document.getElementById('cart-panel');
    cartPanel.classList.add("show");
    if (cartPanel.style.right === '-100vw') {
        cartPanel.style.right = '0'
    } else {
        cartPanel.style.right = '-100vw'
    }
    // Jeśli chcesz automatycznie usunąć "show" po wysunięciu:
    setTimeout(() => {
        cartPanel.classList.remove("show");
        // Można dodać kolejną klasę np. "visible" by utrzymać panel otwarty
    }, 1500);
    animated_cart()
});

function focusOnNewsTab(clict_tab, other_tab) {
    const clict_tab_element = document.getElementById(clict_tab);
    const other_tab_element = document.getElementById(other_tab);

    clict_tab_element.classList.toggle("focus-tab");
    other_tab_element.classList.toggle('hidden');
}

function fiesta() {
    let dance1 = document.createElement('div');
    let dance2 = document.createElement('div');
    let dance3 = document.createElement('div');
    dance1.classList.add('robok1')
    dance2.classList.add('robok2')
    dance3.classList.add('robok3')
    dance1.style.position = 'absolute'
    document.getElementById('dont').appendChild(dance1)
    document.getElementById('dont').appendChild(dance2)
    document.getElementById('dont').appendChild(dance3)
    document.getElementById('fiesta').play()
    document.getElementById('fiesta').addEventListener('ended', function () {
        document.getElementById('dont').innerHTML = ''
    });

}