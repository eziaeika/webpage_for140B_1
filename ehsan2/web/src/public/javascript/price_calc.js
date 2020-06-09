function computeLoan() {
    var amount = document.getElementById('amount').value;
    var interest_rate = 5;

    var interest = (amount * (interest_rate * .01)) / 1;
    var payment = (interest).toFixed(1);
    payment = payment.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    document.getElementById('payment').innerHTML = "Profit = $" + Number(payment).toPrecision(3);



}