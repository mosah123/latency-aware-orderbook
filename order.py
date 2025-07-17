import time
from dataclasses import dataclass

@dataclass
class Order:
    """Represents a single order in the order book."""
    order_id: int
    side: str  # 'buy' or 'sell'
    price: float
    quantity: int
    order_type: str  # 'limit', 'market', 'ioc'
    submission_time: float = None
    arrival_time: float = None # This will be used for time priority

    def __post_init__(self):
        if self.submission_time is None:
            self.submission_time = time.time()
        # arrival_time will be set after latency simulation in main.py

    def __repr__(self):
        latency_ms = (self.arrival_time - self.submission_time) * 1000 if self.arrival_time and self.submission_time else 0
        return (f"Order(id={self.order_id}, side='{self.side}', "
                f"price={self.price:.2f}, qty={self.quantity}, "
                f"type='{self.order_type}', latency={latency_ms:.2f}ms)")
