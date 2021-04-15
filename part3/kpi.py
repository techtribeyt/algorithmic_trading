def get_CAGR(df, periods, price_col_name = "Adj Close"):
    t = len(df) / periods
    return (df[price_col_name][-1] / df[price_col_name][0]) ** (1 / t) - 1

def get_volatility(df_original, periods, price_col_name = "Adj Close"):
    df = df_original.copy()
    df["periodic_return"]= df[price_col_name].pct_change()
    return df["periodic_return"].std() * (periods ** 0.5)

def get_sharpe_ratio(df_original, periods, risk_free_rate = 0.016, price_col_name = "Adj Close"):
    return (get_CAGR(df_original, periods, price_col_name = price_col_name) - risk_free_rate) / get_volatility(df_original, periods, price_col_name = price_col_name)


def get_sortino_ratio(df_original, periods, risk_free_rate = 0.016, price_col_name = "Adj Close"):
    return (get_CAGR(df_original, periods, price_col_name = price_col_name) - risk_free_rate) / get_negative_volatility(df_original, periods, price_col_name = price_col_name)


def get_negative_volatility(df_original, periods, price_col_name = "Adj Close"):
    df = df_original.copy()
    df["periodic_return"]= df[price_col_name].pct_change()
    return df[df["periodic_return"] < 0]["periodic_return"].std() * (periods ** 0.5)

def get_max_drawdown(df_original, price_col_name = "Adj Close"):
    df = df_original.copy()
    df["periodic_return"] = df[price_col_name].pct_change()
    df["cum_return"] = (1 + df["periodic_return"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    return df["drawdown_pct"].max()

def print_strategy_summary(name, periods, df, price_col_name = "Adj Close"):
    print(name)
    print("CAGR: {}".format(get_CAGR(df, periods, price_col_name = price_col_name)))
    print("Volatility: {}".format(get_volatility(df, periods, price_col_name = price_col_name)))
    print("Sharpe Ratio: {}".format(get_sharpe_ratio(df, periods, price_col_name = price_col_name)))
    print("-volatility: {}".format(get_negative_volatility(df, periods, price_col_name = price_col_name)))
    print("Sortino Ratio: {}".format(get_sortino_ratio(df, periods, price_col_name = price_col_name)))
    print("Max Drawdown: {}".format(get_max_drawdown(df, price_col_name = price_col_name)))
