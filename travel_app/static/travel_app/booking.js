
const totalPrice = document.getElementById('totalPrice');
const seatsInput = document.getElementById('id_number_of_seats');

const pricePerSeat = parseFloat(totalPrice.dataset.price);

function updatePrice() {
    const seats = parseInt(seatsInput.value) || 0;
    totalPrice.value = '$' + (seats * pricePerSeat).toFixed(2);
}

seatsInput.addEventListener('input', updatePrice);
updatePrice();
