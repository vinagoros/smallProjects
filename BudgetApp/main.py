import re


class Category:
    def __init__(self, category_name):
        self.category = category_name
        self.ledger = []
        self.balance = 0

    @staticmethod
    def decimal_handling(amount_str):
        decimal = re.search(r"(?<=[0-9][\.])[0-9]*", amount_str)
        if decimal:
            amount_with_decimals = amount_str + "0" * (2 - len(decimal.group(0)))
        else:
            amount_with_decimals = amount_str + ".00"
        return amount_with_decimals

    def __str__(self):
        chars_per_row = 30
        nr_stars = (chars_per_row - len(self.category)) // 2
        output = ["*" * nr_stars + self.category + "*" * nr_stars]
        for movement in self.ledger:
            amount = movement['amount']
            str_amount = str(amount)
            amount_with_decimals = self.decimal_handling(str_amount)
            amount_length = len(amount_with_decimals)
            if (description_length := len(movement['description'])) > 23:
                output.append(movement['description'][:23]
                              + " " * (7 - amount_length) + amount_with_decimals)
            else:
                output.append(movement['description']
                              + " " * (30 - description_length - amount_length)
                              + amount_with_decimals)
        output.append(f"Total: {self.decimal_handling(str(self.balance))}")
        return "\n".join(output)

    def deposit(self, amount, description=""):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount

    def withdraw(self, amount, description=""):
        if balance_check := self.check_funds(amount):
            self.ledger.append({'amount': - amount, 'description': description})
            self.balance -= amount
        return balance_check

    def get_withdrawals(self):
        withdrawals = [movements['amount']
         for movements in self.ledger
         if movements['amount'] < 0]
        print(withdrawals)
        return sum(withdrawals)

    def get_balance(self):
        return self.balance

    def transfer(self, amount, other):
        if balance_check := self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {other.category}')
            other.deposit(amount, f'Transfer from {self.category}')
        return balance_check

    def check_funds(self, amount):
        return amount <= self.balance


def create_spend_chart(categories):
    percentage_space = 5
    max_col_nr = len(categories) * 3 + percentage_space
    lines = ["Percentage spent by category"]
    percentages = list(range(100, -1, -10))
    percentages_lines = [" "*(3-len(str(tenth))) + str(tenth) + "| " for tenth in percentages]
    category_names = []
    category_spending = []
    total = 0
    #mapping percentage of withdrawals
    for category in categories:
        category_names.append(category.category)
        category_withdrawals = category.get_withdrawals()
        category_spending.append(category_withdrawals)
        total += category_withdrawals
    category_spending_percent = [round((spent_in/total)*100) if total < 0 else 0 for spent_in in category_spending]
    #mapping each category to percentage value
    for i, percent in enumerate(percentages):
        for j in range(len(category_names)):
            if category_spending_percent[j] >= percent:
                percentages_lines[i] += "o" + " "*2
            else:
                percentages_lines[i] += " "*3
    lines.extend(percentages_lines)
    #adding final lines
    lines.append(4*" " + "-"*(max_col_nr-4))
    category_max_row_nr = max([len(category) for category in category_names])
    category_lines = [" "*5]*category_max_row_nr
    for i in range(category_max_row_nr):
        for category in category_names:
            if i >= len(category):
                category_lines[i] += " "*3
            else:
                category_lines[i] += category[i] + " "*2
    lines.extend(category_lines)
    return "\n".join(lines)

#TO BE OPTIMIZED

food = Category("Food")
clothing = Category("Clothes")
auto = Category("Auto")
food.deposit(1000)
clothing.deposit(200)
food.withdraw(100)
food.transfer(200, clothing)
clothing.withdraw(400)
auto.deposit(1000)
auto.withdraw(700)
print(create_spend_chart([food, clothing, auto]))