Create an order
    1. The user sends the creation message: @bot + action + items
    2. The bot answers with an item list, an order ID and a confirmation request

Modify an order
    1. The user answers on the creation thread requesting a change: action + {number} + item
    2. The bot answers with a new item list modified

Confirm an order
    1. The user answers to the thread where the order is: send + orderID
    2. The bot sends a message to the channel and thread with the end item list
