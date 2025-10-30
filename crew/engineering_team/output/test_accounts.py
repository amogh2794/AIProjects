import unittest
from accounts import Account, get_share_price


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account = Account(user_id='user123')

    def test_initial_state(self):
        self.assertEqual(self.account.user_id, 'user123')
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
        self.assertEqual(self.account.initial_deposit, 0.0)

    def test_deposit_funds(self):
        self.account.deposit_funds(100.0)
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.initial_deposit, 100.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.account.deposit_funds(50.0)
        self.assertEqual(self.account.balance, 150.0)
        self.assertEqual(self.account.initial_deposit, 100.0)
        self.assertEqual(len(self.account.transactions), 2)

    def test_withdraw_funds(self):
        self.account.deposit_funds(100.0)
        success = self.account.withdraw_funds(50.0)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(len(self.account.transactions), 2)
        fail = self.account.withdraw_funds(100.0)
        self.assertFalse(fail)
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(len(self.account.transactions), 2)

    def test_buy_shares(self):
        self.account.deposit_funds(1000.0)
        success = self.account.buy_shares('AAPL', 5, get_share_price)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 250.0)
        self.assertEqual(self.account.holdings['AAPL'], 5)
        self.assertEqual(len(self.account.transactions), 2)

    def test_sell_shares(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 5, get_share_price)
        success = self.account.sell_shares('AAPL', 5, get_share_price)
        self.assertTrue(success)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings.get('AAPL', 0), 0)
        self.assertEqual(len(self.account.transactions), 3)

    def test_calculate_total_value(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 5, get_share_price)
        total_value = self.account.calculate_total_value(get_share_price)
        self.assertEqual(total_value, 1000.0)

    def test_calculate_profit_or_loss(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 5, get_share_price)
        profit_or_loss = self.account.calculate_profit_or_loss(get_share_price)
        self.assertEqual(profit_or_loss, 0.0)

    def test_get_profit_or_loss_statement(self):
        self.account.deposit_funds(1000.0)
        statement = self.account.get_profit_or_loss_statement(get_share_price)
        self.assertEqual(statement, 'Current Profit/Loss: Profit $0.00')

        self.account.buy_shares('AAPL', 5, get_share_price)
        self.account.sell_shares('AAPL', 5, get_share_price)
        statement = self.account.get_profit_or_loss_statement(get_share_price)
        self.assertEqual(statement, 'Current Profit/Loss: Profit $0.00')


if __name__ == "__main__":
    unittest.main()