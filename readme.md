
# Overview

CLI application for managing expenses\
App stores given expenses in a form of `csv` file

# Features

- Possibility of setting the budget property for a specific month and year (after exceeding the budget, a message will be shown)

- Quick expense summary time, achieved by updating the sums for specific attributes after each expense change

- Expenses are avaliable in `expenses.csv` file in Data/ directory

# How to Use

1. Have Python 3.10+ installed
2. Install dependencies from `requirements.txt`
3. Set the Terminal's current working directory as the `expense-tracker.py` directory, for exapmle by evoking `cd C:\\path\to\expense-tracker`
4. Enter `expense-tracker.py` and choose a proper command
5. Provide arguments required by the command with `--` prefix, e.g. `--description Breakfast`

### Example prompt

`expense-tracker.py add --description Breakfast --amount 20 --category Food` \
`expense-tracker.py delete --id 1` \
`expense-tracker.py enlist`

# Commands

Format: expense-tracker.py command_name `--required_argument1` `--required_argument2` ...

- add `--description`, `--amount`, `--category`
- update `--id`, `--description`, `--amount`, `--category`
- delete `--id`
- delete_all (none)
- enlist (none)
- summarise `--year`, `--month`, `--category` *each argument here is optional, output is based on which arguments were provided
- set_budget `--year`, `--month`, `--budget`
- delete_budget `--year`, `--month`

### Info

You will be given expense ID after adding it, eventually you can view all IDs by evoking `enlist` command \
Arguments order does not have to be preserved \
Additional argument `--date` can be provided to add command, this means that the expense was made, or will be made on the entered date \
Proper date format is `dd.mm.yyyy`

# Licence

This project is licensed under the MIT License \
See [LICENSE](./LICENSE) for more information

# Credits

Idea: https://roadmap.sh/projects/expense-tracker \
Code: https://github.com/piotr-czarnecki07