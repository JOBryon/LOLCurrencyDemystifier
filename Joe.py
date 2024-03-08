# Currency object that holds the name of each currency, the symbol representation and the prices of rp in that currency listed [RP, price] in a list of arrays
class Currency:
    def __init__(self, name, symbol, lol_prices) -> None:
        self.name = name
        self.symbol = symbol
        self.league_prices = lol_prices
    

# Riot points pricing by country from https://leagueoflegends.fandom.com/wiki/RP

# United States Dollar
US_Dollar = Currency("US Dollar","$",[[575, 4.99],[1380,10.99],[2800,21.99],[4500,34.99],[6500,49.99],[13500,99.99]])

# Canadian Dollar
CND_Dollar = Currency("Canadian Dollar","$",[[475, 5.49],[1380,14.99],[2800,29.99],[4800,49.99],[7250,74.99],[13000,129.99]])

# Euro
Euro = Currency("Euro", "€", [[575,4.99],[1380,10.99],[2800,21.99],[4500,34.99],[6500,49.99],[13500,99.99]])

# Great British Pound
GB_Pound = Currency("Great British Pound","£",[[575,4.49],[1450,10.99],[2850,20.99],[5000,34.99],[7250,49.99],[15000,99.99]])

# Polish Ztoty
PL_Ztoty = Currency("Polish złoty", "zł",[[350,13.99],[750,27.99],[1380,47.99],[2950,99.99],[5250,174.99],[10750,349.99]])

# Czech Koruna
CZ_Koruna = Currency("Czech Koruna","Kč",[[325,79],[650,149],[1380,299],[2800,599],[6250,1290],[12500,2490]])

# Romanian New Leu
RMN_New_Leu = Currency("Romanian New Leu", "RON",[[250,9.99],[650,24.99],[1380,49.99],[2800,99.99],[5750,199.99],[12500,429.99]])

# Hungarian Forint
HG_Forint = Currency("Hungarian Forint", "Ft", [[250,799],[650,1990],[1400,3990],[2850,7990],[5500,14990],[11500,29990]])

# Brazil Real
BZ_Real = Currency("Brazilian Real", "R$", [[400,10.90],[1275,34.90],[2575,69.90],[4575,124.90],[6425,174.90],[12850,349.90]])

# Australian Dollar
AU_Dollar = Currency("Australian Dollar", "$", [[475,5.99],[1425,16.99],[2800,30.99],[4600,49.99],[7000,74.99],[12500,129.99]])

# New Zealand Dollar 
NZ_Dollar = Currency("New Zealand Dollar", "$", [[520,6.99],[1380,16.99],[2850,34.99],[4200,49.99],[6500,74.99],[12750,139.99]])

# Finds the cheapest combination of purchases you can make
# Returns a list of two dimensional arrays with [0] being [Total RP you will Receive, Total Price you will pay]
# Every array in the list afterwards is each purchase you will make 
def findCheapestPurchase(target, currency):
    # Initialize total
    total = [[0,0]]
    # Initialize impossibly large last distance to be compared when pathfinding
    lastDistanceReset = [99999999999,[]]
    lastDistance = lastDistanceReset.copy()
    while total[0][0] < target:
        for row in currency:
            # Find the distance from the current total to the target total a purchase of this amount will be
            distance = (target - (row[0] + total[0][0]))
            # If a purchase would put you over the amount of RP you want prioritize spending as little money as 
            # possible and ignore this distance unless it is the smallest amount of currency you can buy
            if (row == currency[0]):
                distance = abs(distance)
            if(distance >= 0):
                if (distance < lastDistance[0]):
                    lastDistance[0] = distance
                    lastDistance[1] = row
            else:
                break
        # Add the purchase onto the list of purchases and increase the running total
        total[0][0] += lastDistance[1][0]
        total[0][1] += lastDistance[1][1]
        total.append(lastDistance[1])
        # Reset last distance
        lastDistance = lastDistanceReset.copy()
    # Round the total cost of the total to 2 digits
    total[0][1] = round(total[0][1], 2)
    return total
    
print(findCheapestPurchase(4600, US_Dollar.league_prices))




