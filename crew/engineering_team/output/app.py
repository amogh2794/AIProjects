import gradio as gr
from accounts import Account, get_share_price


def create_account(user_id):
    global account
    account = Account(user_id)
    return f"Account created for user: {user_id}"


def deposit_funds(amount):
    if amount > 0:
        account.deposit_funds(amount)
        return f"Deposited: ${amount:.2f}"
    else:
        return "Deposit amount must be positive."


def withdraw_funds(amount):
    if amount > 0:
        if account.withdraw_funds(amount):
            return f"Withdrew: ${amount:.2f}"
        else:
            return "Insufficient funds for withdrawal."
    else:
        return "Withdrawal amount must be positive."


def buy_shares(symbol, quantity):
    if quantity > 0:
        if account.buy_shares(symbol, quantity, get_share_price):
            return f"Bought {quantity} shares of {symbol}."
        else:
            return "Insufficient funds to buy shares."
    else:
        return "Quantity must be positive."


def sell_shares(symbol, quantity):
    if quantity > 0:
        if account.sell_shares(symbol, quantity, get_share_price):
            return f"Sold {quantity} shares of {symbol}."
        else:
            return "Insufficient shares to sell."
    else:
        return "Quantity must be positive."


def get_portfolio_value():
    value = account.calculate_total_value(get_share_price)
    return f"Total Portfolio Value: ${value:.2f}"


def get_profit_or_loss():
    return account.get_profit_or_loss_statement(get_share_price)


def get_holdings():
    holdings = account.get_holdings()
    return "Holdings: " + ", ".join([f"{symbol}: {quantity}" for symbol, quantity in holdings.items()])


def get_transaction_history():
    transactions = account.get_transaction_history()
    history = "\n".join([f"{transaction['type'].capitalize()} - {transaction.get('symbol', '')} {transaction.get('quantity', '')} at ${transaction.get('price', ''):.2f}" for transaction in transactions])
    return "Transaction History:\n" + history if transactions else "No transactions yet."


account = None

with gr.Blocks(title="Trading Account") as demo:
    gr.Markdown("## Trading Account Console")

    with gr.Group():
        gr.Markdown("### Create Account")
        user_id = gr.Textbox(label="User ID", value="user1")
        create_btn = gr.Button("Create Account")
        create_status = gr.Textbox(label="Status", interactive=False)
        create_btn.click(create_account, inputs=[user_id], outputs=[create_status])

    with gr.Group():
        gr.Markdown("### Funds")
        amount = gr.Slider(minimum=0, maximum=10000, value=0, label="Amount")
        with gr.Row():
            deposit_btn = gr.Button("Deposit")
            withdraw_btn = gr.Button("Withdraw")
        funds_status = gr.Textbox(label="Funds Status", interactive=False)
        deposit_btn.click(deposit_funds, inputs=[amount], outputs=[funds_status])
        withdraw_btn.click(withdraw_funds, inputs=[amount], outputs=[funds_status])

    with gr.Group():
        gr.Markdown("### Trades")
        symbol = gr.Dropdown(choices=["AAPL", "TSLA", "GOOGL"], label="Stock Symbol", value="AAPL")
        quantity = gr.Slider(minimum=0, maximum=100, value=0, label="Quantity")
        with gr.Row():
            buy_btn = gr.Button("Buy")
            sell_btn = gr.Button("Sell")
        trade_status = gr.Textbox(label="Trade Status", interactive=False)
        buy_btn.click(buy_shares, inputs=[symbol, quantity], outputs=[trade_status])
        sell_btn.click(sell_shares, inputs=[symbol, quantity], outputs=[trade_status])

    with gr.Group():
        gr.Markdown("### Reports")
        with gr.Row():
            value_btn = gr.Button("Portfolio Value")
            pnl_btn = gr.Button("Profit/Loss")
            holdings_btn = gr.Button("Holdings")
            history_btn = gr.Button("Transactions")
        report_box = gr.Textbox(label="Report", lines=8, interactive=False)
        value_btn.click(get_portfolio_value, inputs=None, outputs=[report_box])
        pnl_btn.click(get_profit_or_loss, inputs=None, outputs=[report_box])
        holdings_btn.click(get_holdings, inputs=None, outputs=[report_box])
        history_btn.click(get_transaction_history, inputs=None, outputs=[report_box])

demo.launch()