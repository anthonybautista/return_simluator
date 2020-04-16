from util import get_params, trade, calculate_lt_returns

#get parameters
param = get_params()
start_value = param.portfolio
lt_alloc = param.lt_alloc
st_alloc = param.st_alloc
cash = param.cash_alloc
lt_holding_pct = param.lt_holding_pct
rebalance = param.rebalance_period
lt_holdings = []
lt_returns = 0

#print initial parameters
print('\nInitial Simulation Parameters:')
print('Starting portfolio value: ${:.2f}'.format(start_value))
print('Cash allocation: ${:.2f}'.format(cash*start_value))
print('Long-term allocation: ${:.2f}'.format(lt_alloc*start_value))
print('Rebalance every {} days'.format(rebalance))
if lt_alloc > 0:
    print('Allocation per long-term holding: {:.2f}%'.format(lt_holding_pct * 100))
    print('\nLong-term holdings:')
    for i in range(int((lt_alloc*start_value) / ((lt_alloc*start_value) * lt_holding_pct))):
        lt_holdings.append(((lt_alloc*start_value) * lt_holding_pct))
        print('Stock {}: ${:.2f}'.format(i+1, lt_holdings[i]))
print('\nBegin simulation:\n')

#begin Simulation
day = 0
portfolio = start_value
trade_alloc = st_alloc
trade_size = portfolio * param.trade_size
num_trades = param.n_daytrades
st_returns = []
total_distributions = []

while portfolio > (portfolio * (1 - param.max_loss)):
    #determine trade size
    if param.size_continuous:
        trade_size = portfolio * param.trade_size
        print('Trade size: ${:.2f}'.format(trade_size))
    #calculate day trading profits
    returns = [trade(trade_size, param.st_win_pct, param.st_gain_pct, param.st_loss_pct) for i in range(num_trades)]
    returns = round(sum(returns), 2)
    st_returns.append(returns)
    portfolio += returns
    day += 1
    if portfolio > (portfolio * (1 - param.max_loss)):
        print("Day {} profit: ${:.2f}".format(day, returns))

        #check if targets reached
        if param.end_days:
            if day == param.target_days:
                print('Simulation done after {} days. Final portfolio value is ${:.2f}.'.format(day, portfolio))
                if param.dist_pct > 0:
                    print('Total distributions during simulation: ${:.2f}'.format(sum(total_distributions)))
                break
        else:
            if portfolio >= param.target_value:
                print('Target portfolio value attained after {} days. Final portfolio value is ${:.2f}.'.format(day, portfolio))
                if param.dist_pct > 0:
                    print('Total distributions during simulation: ${:.2f}'.format(sum(total_distributions)))
                break

        #check if rebalance needed
        if day % rebalance != 0:
            pass
        else:
            if lt_alloc > 0:
                lt_holdings, lt_returns = calculate_lt_returns(lt_holdings, param.lt_win_pct, param.lt_gain_pct, param.lt_loss_pct)
                print('\nLong-term holdings:')
                for i in range(len(lt_holdings)):
                    print('Stock {}: ${:.2f}'.format(i+1, lt_holdings[i]))
                    print('Period returns for long-term holdings: ${:.2f}'.format(lt_returns))
                    print('Period returns for short-term holdings: ${:.2f}'.format(sum(st_returns)))
                    portfolio += lt_returns
            period_returns = lt_returns + sum(st_returns)
            st_returns = []
            print('Portfolio balance after {} days: ${:.2f}.\n'.format(day, portfolio))

            #make distributions if necessary
            if param.dist_pct > 0:
                distribution = period_returns * param.dist_pct
                total_distributions.append(distribution)
                print('\nDistributions: ${:.2f}'.format(distribution))
                portfolio -= distribution
                print('New portfolio balance: ${:.2f}'.format(portfolio))

            if lt_alloc > 0:
                lt_holdings = []
                print('New long-term holdings:')
                for i in range(int((lt_alloc*portfolio) / ((lt_alloc*portfolio) * lt_holding_pct))):
                    lt_holdings.append(((lt_alloc*portfolio) * lt_holding_pct))
                    print('Stock {}: ${:.2f}'.format(i+1, lt_holdings[i]))

            #recalculate trade size
            if not param.size_continuous:
                trade_size = portfolio * param.trade_size
                print('--- New trade size: ${:.2f} per trade ---'.format(trade_size))
    else:
        print('You reached your maximum loss. Portfolio amount: {:.2f}'.format(portfolio))
        break