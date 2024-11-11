# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import re

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def starts_with(substring, string):
    string_to_match = "^" + substring + "{1}"
    result = re.match(string_to_match, string)
    return result.group(0)if result else 0
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(starts_with("23", "23_1"))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


False and False