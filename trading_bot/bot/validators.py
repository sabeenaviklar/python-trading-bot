def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValueError("Symbol cannot be empty.")
    return symbol.upper().strip()

def validate_side(side: str) -> str:
    if not side:
        raise ValueError("Side cannot be empty.")
    side = side.upper().strip()
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL.")
    return side

def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValueError("Order type cannot be empty.")
    order_type = order_type.upper().strip()
    if order_type not in ['MARKET', 'LIMIT', 'STOP_MARKET']:
        raise ValueError("Order type must be MARKET, LIMIT, or STOP_MARKET.")
    return order_type

def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError("Quantity must be greater than 0.")
    return quantity

def validate_price(price: float, order_type: str) -> float:
    if order_type == 'LIMIT' and price is None:
        raise ValueError("Price is required for LIMIT orders.")
    if price is not None and price <= 0:
        raise ValueError("Price must be greater than 0.")
    return price

def validate_stop_price(stop_price: float, order_type: str) -> float:
    if order_type == 'STOP_MARKET' and stop_price is None:
        raise ValueError("Stop Price is required for STOP_MARKET orders.")
    if stop_price is not None and stop_price <= 0:
        raise ValueError("Stop Price must be greater than 0.")
    return stop_price
