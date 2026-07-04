import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import logger

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = None

    def connect(self):
        try:
            # Initialize the client and set to testnet
            self.client = Client(self.api_key, self.api_secret, testnet=True)
            # Verify connection by fetching server time
            self.client.futures_time()
            logger.info("Successfully connected to Binance Futures Testnet.")
            return True
        except (BinanceAPIException, BinanceRequestException) as e:
            logger.error(f"Failed to connect to Binance API: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            return False

    def get_client(self):
        return self.client
