import random
import sys
import time
from tabulate import tabulate


class Bank():
    def __init__(self, money):
        self.money = money


class Plot():
    def __init__(self):
        self.nutrients = 1
        self.luck = 0
        self.pest_control = 1
        self.maintenance = 1
        self.lv = 1


plots = []


def main():
    dim, first = getdifficulty()
    terminal = start()
    account = Bank(int(first))
    plot1 = Plot()
    plots.append(plot1)
    season = 0
    freeplay = 0
    start_time = time.time()
    while True:
        season += 1
        print(f"\n\n\nSeason: {season}")
        potato_yield(account, plot1)
        dec_quality(plots, dim)
        if freeplay != 1:
            freeplay = goal(account, terminal, season, freeplay, start_time)
        shop(plot1, account)


def getdifficulty():
    print("Easy:😊\nMedium:😐\nHard:🥵\n")
    while True:
        difficulty = input("Select difficulty: ").strip().lower()
        if difficulty in ["easy", "e"]:
            return (1, 100)
        elif difficulty in ["medium", "normal", "m", "n"]:
            return (1.1, 80)
        elif difficulty in ["hard", "h"]:
            return (1.2, 50)


def start():
    while True:
        try:
            terminal = int(float(input("💵🎯 What is your money goal?🎯💵 $").strip()))
            if terminal:
                if terminal < 111:
                    pass
                else:
                    return terminal
        except (TypeError, ValueError):
            pass


def potato_yield(account, plot1):
    def lose(attribute):
        if attribute == "nutrients":
            sys.exit("💀 Game over!💀 Your garden died due to a lack of nutrients!🥀 Better luck next time!")
        elif attribute == "pest":
            sys.exit("💀 Game over!💀 Your garden was overrun by pests!🐀 Better luck next time!")
        elif attribute == "maintenance":
            sys.exit("💀 Game over!💀 Your garden fell apart due to a lack of maintenance!💔 Better luck next time!")
        elif attribute == "special":
            sys.exit("💀 Game over!💀 Your garden ran out of nutrients, was overrun by pests and fell apart due to lack of maintenance.🥀🐀💔 Better luck next time!")


    amount = random.randint(1, 5 + 5*plot1.lv)
    if plot1.nutrients == 0:
        amount -= int(amount/2)
        condition = random.randint(1, 10)
        if condition == 1 or condition == 2:
            lose("nutrients")
    elif plot1.nutrients < 0.10:
        amount -= int(amount/1.5)
        condition = random.randint(1, 10)
        if condition == 1:
            lose("nutrients")
    if plot1.pest_control == 0:
        amount -= int(amount/2)
        condition = random.randint(1, 10)
        if condition == 1 or condition == 2:
            lose("pest")
    elif plot1.pest_control < 0.10:
        amount -= int(amount/1.5)
        condition = random.randint(1, 10)
        if condition == 1:
            lose("pest")
    if plot1.maintenance == 0:
        amount -= int(amount/2)
        condition = random.randint(1, 10)
        if condition == 1 or condition == 2:
            lose("maintenance")
    elif plot1.maintenance == 0:
        amount -= int(amount/1.5)
        condition = random.randint(1,10)
        if condition == 1:
            lose("maintenance")
    if plot1.nutrients == 0 and plot1.pest_control == 0 and plot1.maintenance == 0:
            lose("special")
    if amount == 1:
        print("You grew 1 potato this season!" + "🥔")
    else:
        print(f"You grew {amount} potatoes this season!" + "🥔" * amount)
    account.money += amount * 1
    print(f"💵 You made ${amount} this season!💵")
    return amount


def dec_quality(plots, scale):
    for plot in plots:
        plot.nutrients = round(plot.nutrients - scale*(random.randint(10, 30)/100), 2)
        if plot.nutrients <= 0:
            plot.nutrients = 0
            print("⚠️ Soil nutrients is 0!⚠️")
        plot.luck -= 0.05
        if plot.luck <= 0:
            plot.luck = 0
        plot.pest_control = round(plot.pest_control - scale*(random.randint(8, 13)/100), 2)
        if plot.pest_control <= 0:
            plot.pest_control = 0
            print("⚠️ Pest control is 0!⚠️")
        plot.maintenance = round(plot.maintenance - scale*(random.randint(3, 8)/100), 2)
        if plot.maintenance <= 0:
            plot.maintenance = 0
            print("⚠️ Plot maintenance is 0!⚠️")


def shop(plot1, account):
    print("What would you like to purchase?")
    table = [["Fertiliser [1]", 10, plot1.nutrients], ["Pest Control [2]", 15, plot1.pest_control], ["Repairs [3]", 20, plot1.maintenance], ["Upgrade [4]", 100, plot1.lv]]
    headers = ["Item", "Price", "Current Status"]
    print(tabulate(table, headers, tablefmt="plain"))
    print(f"Current money: ${account.money}")
    shop = input("Purchase: ")
    if shop == "1":
        if account.money - 10 >= 0:
            plot1.nutrients = 1
            account.money -= 10
        else:
            print("Not enough money!")
        print("Purchase complete!✅ Nutrients refilled!🌱")
    elif shop == "2":
        if account.money - 15 >= 0:
            plot1.pest_control = 1
            account.money -= 15
        else:
            print("Not enough money!")
        print("Purchase complete!✅ Pest control stocked up!🪤")
    elif shop == "3":
        if account.money - 20 >= 0:
            plot1.maintenance = 1
            account.money -= 20
        else:
            print("Not enough money!")
        print("Purchase complete!✅ Garden repaired!🔧")
    elif shop == "4":
        if plot1.lv < 4:
            if account.money - 100 >= 0:
                plot1.lv += 1
                account.money -= 100
                print("Purchase complete!✅ Garden upgraded!⬆️ You can now grow more potatoes!🥔")
            else:
                print("🚫 Not enough money!🚫")
        else:
            print("🟪 Maximum garden level already achieved! Cannot upgrade further.🟪")


def goal(account, terminal, season, freeplay, start_time):
    #checks if user has reached goal
    if account.money >= terminal:
        end_time = time.time()
        elapsed_time = end_time - start_time
        score = round(season / elapsed_time, 4)
        print(f"🏆 Goal achieved!🏆\nYou've made ${account.money}!\nIt took {season} seasons!")
        print(f"📊 Your score: {score}")
        end = input("Do you wish to end the game? [y/n]").strip().lower()
        if end in ["y", "yes"]:
            sys.exit("🕊️ Game over.🕊️")
        else:
            freeplay = 1
            return freeplay
    else:
        pass


if __name__ == "__main__":
    main()
