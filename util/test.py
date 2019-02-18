a = 18600   # 工资
b = 3240    # 三险一金
c = 1000    # 专项扣除
m = 12      # 月份
n = 1       # 第一个月份
moneys = [] # 每个月汇缴的税
sums = []

def sum_money(taxs):
    sum_tax = 0
    for tax in taxs:
        sum_tax += tax
    return sum_tax

for i in range(12):
    sum = (a-b-c-5000)*n
    sums.append(sum)
    n += 1
    if sum <=36000:
        money = sum * 0.03
        moneys.append(money)
    elif 36000 < sum <= 144000:
        money = sum * 0.1-sum_money(moneys)-2520
        moneys.append(money)
    elif 144000 < sum <= 300000:
        money = sum * 0.2-sum_money(moneys)-16920
        moneys.append(money)
    elif 300000 < sum <= 420000:
        money = sum * 0.25-sum_money(moneys)-31920
        moneys.append(money)
    elif 420000 < sum <= 660000:
        money = sum * 0.3-sum_money(moneys)-52920
        moneys.append(money)
    elif 660000 < sum <= 960000:
        money = sum * 0.35-sum_money(moneys)-85920
        moneys.append(money)
    elif sum > 960000:
        money = sum * 0.45-sum_money(moneys)-181920
        moneys.append(money)
    
print(moneys)
print(sum_money(moneys))


