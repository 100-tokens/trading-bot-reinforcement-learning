import numpy as np
import gymnasium as gym
from gymnasium import spaces
import pandas as pd
from portfolio import Portfolio


class StockTradingEnv(gym.Env):
    def __init__(self, data, initial_balance=10000, maker_fee=0.0005, taker_fee=0.0002, slippage_cost=0.01, epsilon=0.1,
                 epsilon_decay=0.995, epsilon_min=0.01):
        super(StockTradingEnv, self).__init__()
        self.data = data
        self.current_step = 0

        # portfolio will manage all trades
        self.portfolio = Portfolio(initial_balance=initial_balance)

        self.date_history = data['time']
        self.open_history = data['high']
        self.high_history = data['high']
        self.low_history = data['low']
        self.close_history = data['close']

        self.maker_fee = maker_fee
        self.taker_fee = taker_fee
        self.slippage_cost = slippage_cost

        #TODO: Preprocess data
        #TODO: normalize data

        # observation space
        self.observation_space = spaces.Box(low=np.inf, high=np.inf, shape=(self.close_history[1],))

        # action space: Buy/Sell signal (-1 to 1) and quantity (0 to 1)
        self.action_space = spaces.Box(low=np.array([-1, 0]), high=np.array([1, 1]), shape=(2,), dtype=np.float32)

        #TODO: inistialize hyperparameters for reward calculations

        # Epsilon-greedy parameters
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min

    def step(self, action):
        # get data of the current step
        open_price = self.open_history(self.current_step)
        high_price = self.high_history[self.current_step]
        low_price = self.low_history[self.current_step]
        close_price = self.close_history[self.current_step]

        # TODO: sizing trade
        # TODO: evaluate portfolio before actions
        # TODO: execute buy/sell actions
        # TODO: evaluate portfolio after actions
        # TODO: calculate reward

        # Record action in rendering
        # self.render(action, quantity, current_portfolio_value)
        obs = self._get_observation()