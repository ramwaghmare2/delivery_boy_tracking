function fetchOrders() {
    fetch('/get_orders')
    .then(response => response.json())
    .then(data => {
        const ordersList = document.getElementById('ordersList');
        ordersList.innerHTML = '';  // Clear the list

        data.orders.forEach(order => {
            const orderItem = document.createElement('li');
            orderItem.textContent = `Order ID: ${order.id}, Customer: ${order.customer_name}, Item: ${order.item_name}, Address: ${order.address}`;

            orderItem.addEventListener('click', () => {
                document.getElementById('actionButtons').style.display = 'block';

                document.getElementById('acceptOrderBtn').onclick = function() {
                    acceptOrder(order.id);
                };
            });

            ordersList.appendChild(orderItem);
        });
    });
}

function acceptOrder(orderId) {
    const deliveryBoyId = document.getElementById('deliveryBoyId').value;

    fetch('/accept_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            order_id: orderId,
            delivery_boy_id: deliveryBoyId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/tracking';  // Redirect to tracking page
        } else {
            alert('Error accepting order');
        }
    })
    .catch(error => {
        console.error('Error accepting order:', error);
    });
}
