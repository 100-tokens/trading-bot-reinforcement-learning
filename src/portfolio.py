import numpy as np
from datetime import datetime


class Portfolio:
    def __init__(self, initial_balance=0):
        self.initial_balance = initial_balance
        self.balance = self.initial_balance  # cash disponible
        self.opened_trades = []
        self.closed_trades = []
        self.evaluation = self.initial_balance  # cash et trades ouverts
        self.performance_history = []

    def open_trade(self, ticker, quantity, price, open_transaction_cost, position):
        trade = Trade(ticker, quantity, price, open_transaction_cost, position)
        if trade.initial_value <= self.balance:
            self.opened_trades.append(trade)
            self.balance -= trade.initial_value

    def close_trade(self, trade, price, close_transaction_cost):
        trade.close_trade(price=price, close_transaction_cost=close_transaction_cost)
        self.balance += trade.value  # on rajoute la valeur du trade au cash disponible
        self.opened_trades.remove(trade)
        self.closed_trades.append(trade)

    def evaluate(self):
        total_trades_evaluation = 0
        for trade in self.opened_trades:
            # Mise à jour de la valeur du trade avec le dernier prix connu
            trade.update_trade(trade.close_price)
            total_trades_evaluation += trade.value
        self.evaluation = total_trades_evaluation + self.balance
        self.track_performance()  # Enregistrer l'évaluation à chaque appel de evaluate()

    def track_performance(self):
        performance = {
            "date": datetime.now(),
            "balance": self.balance,
            "evaluation": self.evaluation
        }
        self.performance_history.append(performance)
        return performance

    def calculate_performance_ratios(self, risk_free_rate=0.01):
        # Convertir les évaluations du portefeuille en rendements journaliers
        returns = [self.performance_history[i]['evaluation'] / self.performance_history[i - 1]['evaluation'] - 1
                   for i in range(1, len(self.performance_history))]

        # Si pas assez de données, retourner None
        if len(returns) < 2:
            return None

        returns = np.array(returns)
        mean_return = np.mean(returns)
        std_dev_return = np.std(returns)

        # Ratio de Sharpe
        sharpe_ratio = (mean_return - risk_free_rate) / std_dev_return if std_dev_return != 0 else None

        # Ratio de Sortino
        downside_risk = np.std([r for r in returns if r < 0])
        sortino_ratio = (mean_return - risk_free_rate) / downside_risk if downside_risk != 0 else None

        # Rendement cumulatif
        cumulative_return = (self.evaluation / self.initial_balance) - 1

        return {
            "sharpe_ratio": sharpe_ratio,
            "sortino_ratio": sortino_ratio,
            "cumulative_return": cumulative_return
        }


class Trade:
    def __init__(self, ticker, quantity, price, open_transaction_cost, position):
        self.ticker = ticker
        self.quantity = quantity
        self.initial_price = price
        self.close_price = price
        self.open_datetime = datetime.now()  # Date et heure d'ouverture du trade
        self.close_datetime = None  # Sera défini lors de la clôture du trade
        self.age = 0  # Sera mis à jour lors de la clôture du trade
        self.position = position  # long ou short
        self.open_transaction_cost = open_transaction_cost
        self.PnL = -open_transaction_cost  # Initialement, le PnL est égal au coût d'ouverture
        self.isOpen = True
        self.max_adverse_excursion = 0
        self.max_favorable_excursion = 0
        self.max_drawdown = 0

        # Calcul initial de la valeur du trade
        if self.position == "long":
            self.value = self.quantity * self.initial_price - open_transaction_cost
        elif self.position == "short":
            self.value = self.quantity * (2 * self.initial_price) - open_transaction_cost
        self.initial_value = self.value
        self.max_value = self.value
        self.min_value = self.value

    def update_trade(self, price):
        self.close_price = price
        if self.position == "long":
            self.value = price * self.quantity
        elif self.position == "short":
            self.value = (self.initial_price - price) * self.quantity + self.initial_value
        self.PnL = self.value - self.initial_value
        self.age = datetime.now() - self.open_datetime

        # Mise à jour des excursions maximales
        self.max_favorable_excursion = max(self.max_favorable_excursion, self.value)
        self.max_adverse_excursion = min(self.max_adverse_excursion, self.value)

        # Mise à jour du drawdown
        if self.value < self.min_value:
            self.min_value = self.value
            self.max_drawdown = self.initial_value - self.min_value

    def close_trade(self, price, close_transaction_cost):
        self.update_trade(price)
        self.value -= close_transaction_cost
        self.PnL -= close_transaction_cost
        self.isOpen = False
        self.close_price = price
        self.close_datetime = datetime.now()  # Date et heure de clôture du trade
        self.age = (self.close_datetime - self.open_datetime).total_seconds()  # Âge du trade en secondes

    def evaluate_trade(self):
        # Calcul du rendement
        return_on_trade = (self.PnL / self.initial_value) * 100

        # Durée du trade en heures
        trade_duration_hours = self.age / 3600

        # Ratio Gain/Perte
        win_loss_ratio = self.PnL / abs(self.max_drawdown) if self.max_drawdown != 0 else None

        # MAE (Maximum Adverse Excursion)
        mae = self.max_adverse_excursion

        # MFE (Maximum Favorable Excursion)
        mfe = self.max_favorable_excursion

        return {
            "return_on_trade": return_on_trade,
            "trade_duration_hours": trade_duration_hours,
            "win_loss_ratio": win_loss_ratio,
            "mae": mae,
            "mfe": mfe,
            "max_drawdown": self.max_drawdown
        }
