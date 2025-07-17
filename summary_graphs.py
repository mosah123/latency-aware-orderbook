import json
import matplotlib.pyplot as plt
import os
import numpy as np

# Load summary JSON
with open("summary_report.json", "r") as f:
    summary = json.load(f)

# Extract order book data
bids = {float(price): qty for price, qty in summary["order_book"]["bids"].items()}
asks = {float(price): qty for price, qty in summary["order_book"]["asks"].items()}

# Sort price levels
sorted_bids = dict(sorted(bids.items(), reverse=True))
sorted_asks = dict(sorted(asks.items()))

os.makedirs("output", exist_ok=True)

# === 1. Bid/Ask Depth Chart ===
plt.figure(figsize=(10, 5))
plt.bar(sorted_bids.keys(), sorted_bids.values(), width=0.05, color='green', label='Bids')
plt.bar(sorted_asks.keys(), sorted_asks.values(), width=0.05, color='red', label='Asks')
plt.xlabel("Price")
plt.ylabel("Order Volume")
plt.title("Bid-Ask Depth Chart")
plt.legend()
plt.tight_layout()
plt.savefig("output/depth_chart.png")
plt.close()

# === 2. Volume Distribution Histogram ===
all_prices = list(bids.keys()) + list(asks.keys())
all_volumes = list(bids.values()) + list(asks.values())
plt.figure(figsize=(10, 5))
plt.hist(all_prices, weights=all_volumes, bins=30, color='blue', edgecolor='black')
plt.xlabel("Price")
plt.ylabel("Volume")
plt.title("Volume Distribution by Price")
plt.tight_layout()
plt.savefig("output/volume_distribution.png")
plt.close()

# === 3. Latency Impact Scatter Plot ===
if "latency_analysis" in summary and summary["latency_analysis"]["filled"]:
    plt.figure(figsize=(10, 6))
    
    filled_latencies = summary["latency_analysis"]["filled"]
    unfilled_latencies = summary["latency_analysis"]["unfilled"]

    # Add jitter for better visualization
    y_filled = np.random.normal(1, 0.05, len(filled_latencies))
    y_unfilled = np.random.normal(0, 0.05, len(unfilled_latencies))

    plt.scatter(filled_latencies, y_filled, alpha=0.5, color='green', label='Filled Taker Orders')
    plt.scatter(unfilled_latencies, y_unfilled, alpha=0.5, color='red', label='Unfilled/Maker Orders')
    
    plt.yticks([0, 1], ['Unfilled/Maker', 'Filled'])
    plt.xlabel("Latency (ms)")
    plt.ylabel("Order Outcome")
    plt.title("Impact of Latency on Order Fill Priority")
    plt.legend()
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig("output/latency_impact.png")
    plt.close()

# === 4. Fill Rate Summary ===
plt.figure(figsize=(5, 4))
labels = ['Fill Rate']
values = [summary["fill_rate"]]
plt.bar(labels, values, color='purple')
plt.ylim(0, 100)
plt.ylabel("Percentage")
plt.title("Fill Rate (%)")
plt.tight_layout()
plt.savefig("output/fill_rate.png")
plt.close()

print("Graphs saved to /output folder.")

# === 5. Flowchart of Design Process ===
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(12, 8))
ax.axis('off')

# Add title
fig.suptitle("Processing Pipeline", fontsize=16, fontweight='bold', y=0.95)

# Define box positions (x, y)
positions = {
    "Order Generation": (0.5, 0.88),
    "Apply Latency": (0.5, 0.74),
    "Matching Engine": (0.5, 0.6),
    "Update Order Book": (0.5, 0.46),
    "Trade Execution": (0.5, 0.32),
    "Generate Metrics": (0.5, 0.18),
    "Visualize Results": (0.5, 0.04)
}

# Draw boxes
for step, (x, y) in positions.items():
    ax.text(
        x, y, step,
        ha='center', va='center',
        bbox=dict(boxstyle="round,pad=0.6", fc="lightblue", ec="black", lw=1.5),
        fontsize=11
    )

# Draw arrows between boxes
keys = list(positions.keys())
for i in range(len(keys) - 1):
    x1, y1 = positions[keys[i]]
    x2, y2 = positions[keys[i + 1]]
    ax.annotate(
        '', xy=(x2, y2 + 0.03), xytext=(x1, y1 - 0.03),
        arrowprops=dict(arrowstyle="->", lw=1.5)
    )

# Save flowchart
plt.tight_layout(rect=[0, 0, 1, 0.94])  # Leave space for the title
plt.savefig("output/design_flowchart.png")
plt.close()
