from order_book import OrderBook

class MatchingEngine:
    """The core matching engine."""
    def __init__(self, order_book: OrderBook):
        self.order_book = order_book
        self.trades = []

    def process_order(self, order):
        """Processes an incoming order."""
        if order.order_type == 'limit':
            self._process_limit_order(order)
        elif order.order_type == 'market':
            self._process_market_order(order)
        elif order.order_type == 'ioc':
            self._process_ioc_order(order)

    def _match_order(self, order, book_side, price_level_key):
        """Generic matching logic for buy and sell orders."""
        filled_quantity = 0
        while order.quantity > 0 and book_side:
            best_price_level = book_side.peekitem(0)
            price = best_price_level[0]
            orders_at_price = best_price_level[1]

            if (order.side == 'buy' and order.price < price) or \
               (order.side == 'sell' and order.price > price):
                break  # Price doesn't cross the spread

            while orders_at_price and order.quantity > 0:
                book_order = orders_at_price[0]
                trade_quantity = min(order.quantity, book_order.quantity)

                self.trades.append({
                    'timestamp': order.arrival_time,
                    'price': book_order.price,
                    'quantity': trade_quantity,
                    'taker_order_id': order.order_id,
                    'maker_order_id': book_order.order_id,
                    'taker_latency_ms': (order.arrival_time - order.submission_time) * 1000,
                })

                order.quantity -= trade_quantity
                book_order.quantity -= trade_quantity
                filled_quantity += trade_quantity

                if book_order.quantity == 0:
                    orders_at_price.pop(0)
            
            if not orders_at_price:
                book_side.popitem(0)
        
        return filled_quantity

    def _process_limit_order(self, order):
        if order.side == 'buy':
            self._match_order(order, self.order_book.asks, 'best_ask')
        else: # sell
            self._match_order(order, self.order_book.bids, 'best_bid')

        if order.quantity > 0:
            self.order_book.add_order(order)

    def _process_market_order(self, order):
        # Market orders don't have a price, so we set it to infinity for matching
        if order.side == 'buy':
            order.price = float('inf')
            self._match_order(order, self.order_book.asks, 'best_ask')
        else: # sell
            order.price = 0
            self._match_order(order, self.order_book.bids, 'best_bid')

    def _process_ioc_order(self, order):
        # Similar to limit, but any remaining quantity is cancelled
        if order.side == 'buy':
            self._match_order(order, self.order_book.asks, 'best_ask')
        else: # sell
            self._match_order(order, self.order_book.bids, 'best_bid')
        # Remaining quantity is not added to the book (i.e., cancelled)
