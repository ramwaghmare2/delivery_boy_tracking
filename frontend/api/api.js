function acceptOrder(orderId, deliveryBoyId) {
    return fetch('/accept_order', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: orderId, delivery_boy_id: deliveryBoyId }),
    }).then(response => response.json());
}

function updateStatus(orderId, status) {
    return fetch('/update_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: orderId, status: status }),
    }).then(response => response.json());
}
