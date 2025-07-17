from collections import defaultdict
from sortedcontainers import SortedDict

class OrderBook:
    """Maintains the limit order book."""
    def __init__(self):
        # Bids are sorted from highest to lowest price
        self.bids = SortedDict(lambda price: -price)
        # Asks are sorted from lowest to highest price
        self.asks = SortedDict()

    def add_order(self, order):
        """Adds a limit order to the book."""
        if order.side == 'buy':
            if order.price not in self.bids:
                self.bids[order.price] = []
            self.bids[order.price].append(order)
        else:
            if order.price not in self.asks:
                self.asks[order.price] = []
            self.asks[order.price].append(order)

    def get_best_bid(self):
        return self.bids.peekitem(0)[0] if self.bids else None

    def get_best_ask(self):
        return self.asks.peekitem(0)[0] if self.asks else None

    def __str__(self):
        book_str = "--- Order Book ---\n"
        book_str += "Asks:\n"
        for price, orders in reversed(self.asks.items()):
            total_qty = sum(o.quantity for o in orders)
            book_str += f"  Price: {price:.2f}, Qty: {total_qty}\n"

        book_str += "Bids:\n"
        for price, orders in self.bids.items():
            total_qty = sum(o.quantity for o in orders)
            book_str += f"  Price: {price:.2f}, Qty: {total_qty}\n"
        book_str += "------------------\n"
        return book_str
