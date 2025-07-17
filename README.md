# Trade Lifecycle Simulation and Latency Impact Analysis

This project simulates a trading environment to analyze how latency, order placement, and order book dynamics affect execution performance. It is designed for research and technical demonstration purposes, particularly for roles in quantitative development and trading infrastructure.

## Project Objectives

- Simulate an order book with realistic maker and taker order flow.
- Track the full lifecycle of orders from placement to execution.
- Measure the impact of latency on execution priority.
- Produce a structured report with both visualizations and summary statistics.

## Core Files

| File | Description |
|------|-------------|
| `main.py` | Runs the simulation and generates trade logs and summary output. |
| `order.py` | Defines the structure of an order, including price, side, quantity, and timestamp. |
| `order_book.py` | Manages order queues and the matching process. |
| `matching_engine.py` | Implements the logic for executing orders against the book. |
| `summary_report.json` | Stores aggregated statistics from the simulation. |
| `summary_graphs.py` | Parses the summary report and generates analysis plots. |

## Output Visualizations

1. **Bid-Ask Depth Chart (`depth_chart.png`)**  
   Bar chart showing volume at each bid and ask price level.  
   Interprets market depth and liquidity distribution.

2. **Volume Distribution Histogram (`volume_distribution.png`)**  
   Histogram of total volume across price levels.  
   Highlights concentration of trading activity.

3. **Latency Impact Scatter Plot (`latency_impact.png`)**  
   Scatter plot showing how order latency correlates with fill outcomes.  
   Demonstrates latency-sensitive behavior in execution.

4. **Fill Rate Summary (`fill_rate.png`)**  
   Bar chart showing percentage of orders that were successfully filled.  
   Measures overall system efficiency.

## Summary Report (`summary_report.json`)

This file contains the key statistics generated after the simulation, including:

- Total number of orders and trades
- Fill rate (as a percentage)
- Volume-weighted average price (VWAP)
- Minimum and maximum trade prices
- Final bid-ask spread
- Full bid and ask depth of the order book
- Latency analysis, separating filled and unfilled orders by latency

## Purpose

This project quantifies the effect of millisecond-level latency differences on execution priority in a simulated trading environment. It highlights how low-latency infrastructure can be a competitive advantage in order execution systems.