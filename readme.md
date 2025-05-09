
# Overview

CLI application for managing expenses\
App stores given expenses in a form of the `csv` file

## Features

- Possibility to set the budget property for a specific month and year (after exceeding the budget, a message will be shown)

- Quick expense summary time, achieved by updating the sums for specific attributes after each expense change

- Expenses are avaliable in `expenses.csv` file in `Data\` directory

# How to Use

1. Set the Command Prompt's current directory as the file `expense-tracker.py` directory
2. Enter file's name `expense-tracker.py`
3. Choose a proper command
4. Provide required arguments with `--` prefix, e.g. `--description`

# Commands

Format: command_name `--required_argument1` `--required_argument2` etc.

- add `--description`, `--amount`, `--category`
- update `--id`, `--description`, `--amount`, `--category`
- delete `--id`
- delete_all (none)
- enlist (none)
- summarise `--year`, `--month`, `--category` *each argument here is optional, output is based on which arguments were provided
- set_budget `--year`, `--month`, `--budget`
- delete_budget `--year`, `--month`

### Info

Arguments order does not have to be preserved\
Additional argument `--date` can be provided to add command, this means that the expense was made, or will be made on the entered date\
Proper date format is `dd.mm.yyyy`

# Credits

Idea: https://roadmap.sh/projects/expense-tracker \
Code: https://github.com/piotr-czarnecki-dev