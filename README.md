# Project Setup

This guide will help you set up a virtual environment and install the required dependencies for this project.

## Prerequisites

Ensure you have the following installed on your system:
- **Python 3.6+**: You can check if Python is installed by running `python --version` or `python3 --version` in your terminal.
- **pip**: Python's package installer. Verify installation by running `pip --version`.


# Getting Started
## Clone the Repository
```bash
git clone https://github.com/TempleTradingTechnology/OwlHack_2024_Finance_Challenge.git
cd OwlHack_2024_Finance_Challenge
```

## Setting up the Virtual Environment

1. **Create a Virtual Environment**

   Open your terminal and navigate to the project directory, then run the following command to create a virtual environment:

   ```bash
   python3 -m venv venv
    ```


2. **Activate the Virtual Environment**
- On macOS/Linux:
    ```bash
    . .venv/bin/activate
    ```

- On windows:
    ```bash
    .venv\Scripts\activate
    ```
3. **Install the Required Dependencies**

    With the virtual environment activated, run the following command to install all dependencies listed in requirements.txt:

    ```bash
    pip install -r requirements.txt
    ```



# Backtesting Framework

This framework is designed to help you easily backtest trading strategies with minimal effort. The core idea is that you only need to **focus on writing your custom strategy**, and everything else is handled by the framework.

## Getting Started

1. **Write Your Custom Strategy**: 
   Create your own strategy in the `CustomStrategy.py` file. This is the only place where you need to implement your trading logic.

2. **Run the Backtest**:
   Once your custom strategy is written, simply run the `run_backtest.py` script. It will:
   - Execute the backtest using your strategy
   - Generate performance metrics like Cumulative Return, Sharpe Ratio, and Maximum Drawdown
   - Output trading signals into a CS file

## More In-Depth Guide

For a detailed step-by-step guide on how to set up and use the framework, visit our [Notion page](https://plump-camp-1d8.notion.site/OwlHack-2024-Finance-Challenge-API-fb708316ea864458be9bc5652c4c25eb?pvs=74).

