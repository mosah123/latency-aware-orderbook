import random
import time
import numpy as np
import json
from datetime import datetime
from order import Order
from order_book import OrderBook
from matching_engine import MatchingEngine

def generate_random_order(order_id):
    """Generates a random order."""
    side = random.choice(['buy', 'sell'])
    order_type = random.choices(['limit', 'market', 'ioc'], weights=[0.7, 0.15, 0.15], k=1)[0]
    
    # Generate price around a baseline, e.g., 100
    price = round(random.normalvariate(100, 2), 2)
    quantity = random.randint(1, 100)
    
    return Order(
        order_id=order_id,
        side=side,
        price=price,
        quantity=quantity,
        order_type=order_type
        # submission_time is set on creation
    )

def generate_summary_data(engine: MatchingEngine, all_orders: list):
    """Gathers all summary statistics into a dictionary."""
    summary = {}
    trades = engine.trades
    book = engine.order_book
    total_orders = len(all_orders)

    summary["total_orders"] = total_orders
    summary["total_trades"] = len(trades)

    # Store latency info for analysis
    filled_taker_ids = {t['taker_order_id'] for t in trades}
    summary["latency_analysis"] = {
        "filled": [],
        "unfilled": []
    }
    for order in all_orders:
        latency_ms = (order.arrival_time - order.submission_time) * 1000
        if order.order_id in filled_taker_ids:
            summary["latency_analysis"]["filled"].append(latency_ms)
        else:
            summary["latency_analysis"]["unfilled"].append(latency_ms)


    if not trades:
        summary["fill_rate"] = 0.0
        summary["vwap"] = None
        summary["price_range"] = {"min": None, "max": None}
    else:
        total_volume = sum(t['quantity'] for t in trades)
        trade_prices = [t['price'] for t in trades]
        summary["fill_rate"] = round((len(trades) / total_orders) * 100, 2)
        summary["vwap"] = round(sum(t['price'] * t['quantity'] for t in trades) / total_volume, 2) if total_volume > 0 else 0
        summary["price_range"] = {"min": min(trade_prices), "max": max(trade_prices)}

    best_bid = book.get_best_bid()
    best_ask = book.get_best_ask()
    summary["spread"] = round(best_ask - best_bid, 2) if best_bid and best_ask else None

    summary["order_book"] = {
        "bids": {str(price): sum(o.quantity for o in orders) for price, orders in book.bids.items()},
        "asks": {str(price): sum(o.quantity for o in orders) for price, orders in book.asks.items()}
    }
    return summary

def save_summary_to_json(summary_data: dict, filename="summary_report.json"):
    """Saves the summary report to a JSON file."""
    report = summary_data.copy()
    report["timestamp"] = datetime.now().isoformat()
    
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nSummary report saved to {filename}")

def print_summary_report(summary_data: dict):
    """Prints a summary of the trading session from a data dictionary."""
    print("\n--- Trading Session Summary ---")
    print(f"Total Orders Processed: {summary_data['total_orders']}")
    print(f"Total Trades Executed: {summary_data['total_trades']}")

    if summary_data['total_trades'] == 0:
        print("No trades were executed.")
        return

    print(f"Total Volume Traded: {sum(t['quantity'] for t in engine.trades)}")
    print(f"VWAP: {summary_data['vwap']:.2f}")
    print(f"Fill Rate: {summary_data['fill_rate']:.2f}%")

    if summary_data['spread'] is not None:
        best_bid = engine.order_book.get_best_bid()
        best_ask = engine.order_book.get_best_ask()
        print(f"Final Spread: {summary_data['spread']:.2f} (Bid: {best_bid:.2f}, Ask: {best_ask:.2f})")
    
    print("-----------------------------\n")


if __name__ == "__main__":
    try:
        import sortedcontainers
    except ImportError:
        print("Please install sortedcontainers: pip install sortedcontainers")
        exit()

    # 1. Setup
    order_book = OrderBook()
    engine = MatchingEngine(order_book)
    num_orders_to_simulate = 1000

    # 2. Simulation Loop
    print(f"Generating {num_orders_to_simulate} orders...")
    # Step 1: Generate all orders with their submission times
    orders_to_process = [generate_random_order(order_id=i + 1) for i in range(num_orders_to_simulate)]

    # Step 2: Simulate latency and assign arrival times
    for order in orders_to_process:
        latency = random.uniform(0.000001, 0.005) # Latency from 1us to 5ms
        order.arrival_time = order.submission_time + latency

    # Step 3: Sort orders by arrival time to simulate race conditions
    orders_to_process.sort(key=lambda o: o.arrival_time)

    print("Simulating market...")
    for order in orders_to_process:
        engine.process_order(order)
    print("Simulation complete.")

    # 3. Final State and Report
    print("\nFinal Order Book State:")
    print(order_book)
    
    summary_data = generate_summary_data(engine, orders_to_process)
    print_summary_report(summary_data)
    save_summary_to_json(summary_data)
