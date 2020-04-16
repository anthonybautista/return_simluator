import argparse
from random import randrange as r

#get all parameters for simulation
def get_params():
    parser = argparse.ArgumentParser()

    parser.add_argument('--portfolio', type = int, default = 25000, help = 'Portfolio starting amount')
    parser.add_argument('--lt_alloc', type = float, default = .80, help = 'Percentage of portfolio to allocate towards long-term holdings.')
    parser.add_argument('--st_alloc', type = float, default = .20, help = 'Percentage of portfolio to allocate towards short-term trading.')
    parser.add_argument('--cash_alloc', type = float, default = 0.0, help = 'Percentage of portfolio to allocate towards cash. Not used for trading.')
    parser.add_argument('--lt_holding_pct', type = float, default = 0.20, help = 'Percentage of allocation per holding in long-term portfolio.')
    parser.add_argument('--lt_win_pct', type = float, default = 0.75, help = 'Percentage of long-term holdings that will have positive returns.')
    parser.add_argument('--st_win_pct', type = float, default = 0.50, help = 'Percentage of short-term trades that will have positive returns.')
    parser.add_argument('--lt_gain_pct', type = float, default = 0.04, help = 'Percentage return of winning long-term holdings at each rebalancing.')
    parser.add_argument('--st_gain_pct', type = float, default = 0.30, help = 'Percentage return of winning short-term trades.')
    parser.add_argument('--lt_loss_pct', type = float, default = 0.04, help = 'Percentage loss of losing long-term holdings at each rebalancing.')
    parser.add_argument('--st_loss_pct', type = float, default = 0.20, help = 'Percentage loss of losing short-term trades.')
    parser.add_argument('--n_daytrades', type = int, default = 5, help = 'Number of short-term trades each day.')
    parser.add_argument('--rebalance_period', type = int, default = 21, help = 'Number of days before rebalancing.')
    parser.add_argument('--size_continuous', action = "store_true", default = False, help = 'Short-term trade size will be calculated each day.')
    parser.add_argument('--trade_size', type = float, default = 0.02, help = 'Short-term trade size based on entire portfolio value.')
    parser.add_argument('--end_days', action = "store_true", default = False, help = 'End simulation after a certain number of days.')
    parser.add_argument('--target_days', type = int, default = 252, help = 'Number of days before ending simulation.')
    parser.add_argument('--target_value', type = int, default = 100000, help = 'Portfolio value before ending simulation.')
    parser.add_argument('--max_loss', type = float, default = 0.20, help = 'Maximum percentage loss before ending simulation.')
    parser.add_argument('--dist_pct', type = float, default = 0.0, help = 'Percentage of profits to distribute at rebalancing.')

    return parser.parse_args()

#define simulated trading
def trade(amount, prob, win, loss):
    if r(1,11) <= (prob * 10):
        return amount * win
    else:
        return (amount * loss) * -1

#define long-term returns calculation function
def calculate_lt_returns(lt_holdings, lt_win_pct, lt_gain_pct, lt_loss_pct):
    #lt_holdings should be a list of holding values
    #calculate long-term holding returns
    basis = sum(lt_holdings)
    for i in range(len(lt_holdings)):
        if r(1,11) <= (lt_win_pct * 10):
            lt_holdings[i] += lt_holdings[i] * lt_gain_pct
        else:
            lt_holdings[i] -= lt_holdings[i] * lt_loss_pct
    returns = (sum(lt_holdings) - basis)
    return lt_holdings, returns
