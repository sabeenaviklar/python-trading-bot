from binance.exceptions import BinanceAPIException, BinanceRequestException
from .client import BinanceTestnetClient
from .logging_config import logger

def place_order(client: BinanceTestnetClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None, dry_run: bool = False):
    try:
        binance_client = client.get_client()
        if not binance_client:
            raise ValueError("Client is not connected.")

        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }

        if order_type == 'LIMIT':
            params['timeInForce'] = 'GTC'
            params['price'] = price
        elif order_type == 'STOP_MARKET':
            params['stopPrice'] = stop_price
            
        if dry_run:
            logger.info(f"[DRY RUN] Would place order: {params}")
            return {
                'success': True,
                'data': {
                    'orderId': 'DRY-RUN-12345',
                    'status': 'SIMULATED',
                    'executedQty': '0.0',
                    'avgPrice': '0.0',
                    'note': 'This was a dry run. No actual API call was made.'
                }
            }
            
        logger.info(f"Placing order request: {params}")
        
        response = binance_client.futures_create_order(**params)
        
        logger.info(f"Order successfully placed: {response}")
        return {
            'success': True,
            'data': response
        }

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception while placing order: {e.status_code} - {e.message}")
        return {'success': False, 'error': f"API Error: {e.message}"}
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception: {e}")
        return {'success': False, 'error': "Network error while connecting to Binance."}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {'success': False, 'error': str(e)}
