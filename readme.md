
# Overview

CLI application for managing expenses.  
The app stores given expenses in the form of a `csv` file.

# Features

- Ability to set a budget for a specific month and year (a message will be shown if the budget is exceeded).
- Quick expense summary achieved by updating the sums for specific attributes after each expense change.
- Expenses are available in the `expenses.csv` file located in the `Data/` directory.

# How to Use

1. Ensure Python 3.10+ is installed.
2. Install dependencies from `requirements.txt`.
3. Set the Terminal's current working directory to the directory containing `expense-tracker.py`, for example, by running `cd C:\\path\to\expense-tracker`.
4. Enter `expense-tracker.py` and choose a proper command.
5. Provide arguments required by the command with the `--` prefix, e.g., `--description Breakfast`.

### Example Prompt

```bash
expense-tracker.py add --description Breakfast --amount 20 --category Food
expense-tracker.py delete --id 1
expense-tracker.py enlist
```

# Commands

Format: `expense-tracker.py command_name --required_argument1 --required_argument2 ...`

- `add` `--description`, `--amount`, `--category`
- `update` `--id`, `--description`, `--amount`, `--category`
- `delete` `--id`
- `delete_all` (no arguments)
- `enlist` (no arguments)
- `summarise` `--year`, `--month`, `--category` *(each argument is optional; output is based on the provided arguments) (month should be in integer format)*
- `set_budget` `--year`, `--month`, `--budget`
- `delete_budget` `--year`, `--month`

### Info

- You will be given an expense ID after adding it. Alternatively, you can view all IDs by running the `enlist` command.  
- The order of arguments does not need to be preserved.  
- An additional argument `--date` can be provided to the `add` command, indicating the date the expense was made or will be made.  
- The proper date format is `dd.mm.yyyy`.

# Licence

This project is licensed under the MIT License \
See [LICENSE](./LICENSE) for more information

# Credits

Idea: https://roadmap.sh/projects/expense-tracker \
Code: https://github.com/piotr-czarnecki07