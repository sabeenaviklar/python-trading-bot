import click
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from dotenv import load_dotenv

# Ensure the bot package is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.client import BinanceTestnetClient
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price, validate_stop_price
from bot.orders import place_order
from bot.logging_config import logger

console = Console()

def load_credentials():
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        console.print("[yellow]API credentials not found in environment or .env file.[/yellow]")
        api_key = Prompt.ask("Enter your Binance Futures Testnet API Key")
        api_secret = Prompt.ask("Enter your Binance Futures Testnet API Secret", password=True)
        
        save = Confirm.ask("Do you want to save these credentials to a .env file?")
        if save:
            env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
            with open(env_path, 'w') as f:
                f.write(f"BINANCE_API_KEY={api_key}\n")
                f.write(f"BINANCE_API_SECRET={api_secret}\n")
            console.print("[green]Credentials saved to .env file.[/green]")
            
    return api_key, api_secret

@click.command()
@click.option('--symbol', prompt=True, help='Trading symbol, e.g., BTCUSDT')
@click.option('--side', type=click.Choice(['BUY', 'SELL'], case_sensitive=False), prompt=True, help='Order side: BUY or SELL')
@click.option('--order-type', type=click.Choice(['MARKET', 'LIMIT', 'STOP_MARKET'], case_sensitive=False), prompt="Order Type (MARKET/LIMIT/STOP_MARKET)", help='Order type: MARKET, LIMIT, STOP_MARKET')
@click.option('--quantity', prompt=True, type=float, help='Order quantity')
@click.option('--price', type=float, default=None, help='Price for LIMIT orders')
@click.option('--stop-price', type=float, default=None, help='Stop price for STOP_MARKET orders')
@click.option('--dry-run', is_flag=True, help='Simulate order placement without calling the API')
def main(symbol, side, order_type, quantity, price, stop_price, dry_run):
    """
    CLI application to place orders on Binance Futures Testnet.
    """
    console.print(Panel.fit("[bold blue]Binance Futures Testnet Trading Bot[/bold blue]"))
    
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        logger.warning(f"User input validation failed: {e}")
        return

    if order_type == 'LIMIT' and price is None:
        price = Prompt.ask("Enter the LIMIT price", type=float)
        
    if order_type == 'STOP_MARKET' and stop_price is None:
        stop_price = Prompt.ask("Enter the STOP price", type=float)

    try:
        price = validate_price(price, order_type)
        stop_price = validate_stop_price(stop_price, order_type)
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        logger.warning(f"User input validation failed: {e}")
        return

    table = Table(title="Order Summary")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="magenta")
    
    table.add_row("Symbol", symbol)
    table.add_row("Side", side)
    table.add_row("Type", order_type)
    table.add_row("Quantity", str(quantity))
    if price:
        table.add_row("Price", str(price))
    if stop_price:
        table.add_row("Stop Price", str(stop_price))
        
    console.print(table)
    
    if not Confirm.ask("Do you want to proceed with placing this order?"):
        console.print("[yellow]Order cancelled by user.[/yellow]")
        logger.info("Order placement cancelled by user.")
        return

    api_key, api_secret = load_credentials()
    
    with console.status("[bold green]Connecting to Binance Testnet...") as status:
        client = BinanceTestnetClient(api_key, api_secret)
        connected = client.connect()
        
    if not connected:
        console.print("[bold red]Failed to connect to Binance Testnet. Check logs for details.[/bold red]")
        return
        
    with console.status(f"[bold green]Placing {order_type} order...") as status:
        result = place_order(client, symbol, side, order_type, quantity, price, stop_price, dry_run=dry_run)
        
    if result['success']:
        data = result['data']
        console.print("\n[bold green]✅ Order Successfully Placed![/bold green]")
        
        res_table = Table(title="Order Response Details")
        res_table.add_column("Field", style="cyan")
        res_table.add_column("Value", style="green")
        
        res_table.add_row("Order ID", str(data.get('orderId')))
        res_table.add_row("Status", str(data.get('status')))
        res_table.add_row("Executed Qty", str(data.get('executedQty')))
        if data.get('avgPrice') and float(data.get('avgPrice', 0)) > 0:
            res_table.add_row("Avg Price", str(data.get('avgPrice')))
        if data.get('note'):
            res_table.add_row("Note", f"[yellow]{data.get('note')}[/yellow]")
            
        console.print(res_table)
    else:
        console.print(f"\n[bold red]❌ Order Failed:[/bold red] {result['error']}")

if __name__ == '__main__':
    main()
