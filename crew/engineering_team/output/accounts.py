def get_share_price(symbol: str) -> float:
    prices = {
        'AAPL': 150.0,
        'TSLA': 650.0,
        'GOOGL': 2800.0,
    }
    return prices.get(symbol, 0.0)

class Account:
    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self.balance = 0.0
        self.holdings = {}
        self.transactions = []
        self.initial_deposit = 0.0

    def deposit_funds(self, amount: float) -> None:
        if self.initial_deposit == 0:
            self.initial_deposit = amount
        self.balance += amount
        self.transactions.append({
            'type': 'deposit',
            'amount': amount
        })
    
    def withdraw_funds(self, amount: float) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            self.transactions.append({
                'type': 'withdrawal',
                'amount': amount
            })
            return True
        return False

    def buy_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        price = get_share_price(symbol) * quantity
        if self.balance >= price:
            self.balance -= price
            if symbol in self.holdings:
                self.holdings[symbol] += quantity
            else:
                self.holdings[symbol] = quantity
            self.transactions.append({
                'type': 'buy',
                'symbol': symbol,
                'quantity': quantity,
                'price': price
            })
            return True
        return False

    def sell_shares(self, symbol: str, quantity: int, get_share_price: callable) -> bool:
        if symbol in self.holdings and self.holdings[symbol] >= quantity:
            price = get_share_price(symbol) * quantity
            self.balance += price
            self.holdings[symbol] -= quantity
            if self.holdings[symbol] == 0:
                del self.holdings[symbol]
            self.transactions.append({
                'type': 'sell',
                'symbol': symbol,
                'quantity': quantity,
                'price': price
            })
            return True
        return False

    def calculate_total_value(self, get_share_price: callable) -> float:
        total_value = self.balance
        for symbol, quantity in self.holdings.items():
            total_value += get_share_price(symbol) * quantity
        return total_value

    def calculate_profit_or_loss(self, get_share_price: callable) -> float:
        return self.calculate_total_value(get_share_price) - self.initial_deposit

    def get_holdings(self) -> dict:
        return self.holdings

    def get_transaction_history(self) -> list:
        return self.transactions

    def get_profit_or_loss_statement(self, get_share_price: callable) -> str:
        profit_or_loss = self.calculate_profit_or_loss(get_share_price)
        statement = f"Current Profit/Loss: {'Profit' if profit_or_loss >= 0 else 'Loss'} ${abs(profit_or_loss):.2f}"
        return statement