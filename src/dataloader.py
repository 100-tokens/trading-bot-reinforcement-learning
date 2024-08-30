from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit


def retrieve_crypto_historical(symbol="BTC/USD", start_date="2020-01-01", end_date="2024-08-08"):
    # Initialiser le client Alpaca
    client = CryptoHistoricalDataClient()
    request_params = CryptoBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame(5, TimeFrameUnit('Min')),
        start=start_date,
        end=end_date
    )


    # Récupérer les données de prix
    btc_bars = client.get_crypto_bars(request_params)

    # Convertir les données en DataFrame
    df = btc_bars.df

    return df
