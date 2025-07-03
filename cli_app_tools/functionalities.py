from datetime import datetime
import pandas
import os
import json
import csv

class Tracker:

    def __init__(self):
        self._cur_path = os.getcwd()
        self._dt = datetime.now().strftime('%d.%m.%Y')

    def add(self, set_id=-1, **kwargs):
        # Set variables from kwargs
        amount = kwargs.get('amount')
        category = kwargs.get('category')
        dsc = kwargs.get('dsc')

        # Check user's custom date if provided
        date = kwargs.get('date')
        if date is not None:
            self._set_date(date)

        # Check data
        if None in (amount, category, dsc):
            print("Not all necessary arguments were provided.")
            return

        try:
            amount = float(amount)
        except ValueError:
            print("Amount must be a number.")
            return

        if amount < 0:
            print("Amount must be a positive number.")
            return

        tokens = self._dt.split('.') # returns a list: year[0] - day, year[1] - month, year[2] - year, each element as a string

        # load setting.json and set variables
        try:
            with open(f"{self._cur_path}\\Data\\settings.json") as file:
                settings = json.load(file)

            budget = settings["budget"][tokens[2]][int(tokens[1]) - 1] # get the budget for the current month
            month_expenses = settings["amounts"][tokens[2]]["month"][int(tokens[1]) - 1]
            if set_id == -1:
                last_id = settings["last_id"]
            else:
                last_id = set_id - 1

        except FileNotFoundError or json.decoder.JSONDecodeError:
            try:
                os.mkdir(f"{self._cur_path}\\Data")
            except OSError:
                pass

            settings = {
                "budget" : {
                    tokens[2] : [-1 for i in range(12)],
                },
                "last_id" : 0,
                "amounts" : {
                    tokens[2] : {
                        "month" : [float(0) for i in range(12)],
                        "category" : dict() # dictionary with a list of expenses made each month mapped to the category (as a string)
                    }
                }
            }
            with open(f"{self._cur_path}\\Data\\settings.json", 'w') as file:
                file.write(json.dumps(settings)) # creates settings file with initial values

            budget = -1 # initial values
            month_expenses = 0
            if set_id == -1:
                last_id = 0
            else:
                last_id = set_id - 1

        except KeyError: # first appear for a new year
            settings["budget"][tokens[2]] = [-1 for i in range(12)]
            settings["amounts"][tokens[2]] = dict()
            settings["amounts"][tokens[2]]["month"] = [0 for i in range(12)]
            settings["amounts"][tokens[2]]["category"] = dict()

            with open(f"{self._cur_path}\\Data\\settings.json", 'w') as file:
                file.write(json.dumps(settings))

            budget = -1
            month_expenses = 0
            if set_id == -1:
                last_id = settings["last_id"]
            else:
                last_id = set_id - 1

        # check if the user isn't exceeding the budget for current month [O(1) time complexity (approximately)]
        if budget != -1 and amount >= budget:
            print("\n\n!!!Set budget for the current month had been exceeded!!!\n\n")
        elif budget != -1 and month_expenses != 0:
            if month_expenses + amount >= budget:
                print("\n\n!!!Set budget for the current month had been exceeded!!!\n\n")

        # write to expenses.csv and create that file if needed
        if not os.path.exists(f"{self._cur_path}\\Data\\expenses.csv"):
            with open(f"{self._cur_path}\\Data\\expenses.csv", 'w', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["ID", "Date", "Description", "Category", "Amount"])
                writer.writerow([last_id + 1, self._dt, dsc, category, amount])
        else:
            with open(f"{self._cur_path}\\Data\\expenses.csv", 'a', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow([last_id + 1, self._dt, dsc, category, amount])

        if set_id == -1:
            print("Expense added successfully (ID: " + str(last_id + 1) + ").")
        else:
            print("Expense updated successfully (ID: " + str(last_id + 1) + ").")

        if set_id == -1 or set_id > int(settings["last_id"]): # update last_id parameter
            self._update_settings(last_id=last_id+1, amount=amount, category=category, year=tokens[2], month=int(tokens[1]))
        else: # don't update
            self._update_settings(amount=amount, category=category, year=tokens[2], month=int(tokens[1]))

    def update(self, **kwargs):
        # Set variables from kwargs
        amount = kwargs.get('amount')
        category = kwargs.get('category')
        dsc = kwargs.get('dsc')
        id_number = kwargs.get('id_number')

        # Check user's custom date if provided
        date = kwargs.get('date')
        if date is not None:
            self._set_date(date)

        # Check cases
        if None in (amount, category, dsc, id_number):
            print("Not all necessery arguments were provided.")
            return

        try:
            id_number = int(id_number)

        except ValueError:
            print("ID must be a number.")
            return

        if id_number < 1:
            print("ID must be a positive integer number (greater than 0).")
            return

        # get settings["last_id"]
        try:
            with open(f"{self._cur_path}\\Data\\settings.json") as file:
                settings = json.load(file)

        except FileNotFoundError or json.decoder.JSONDecodeError:
            print("No expenses has been added yet, or expenses.csv file directory had been changed\nInitial directory (" + self._cur_path + "\\Data).")
            return

        self.delete(self_executed=True, id_number=id_number) # delete previous instance of expense if it exists
        self.add(set_id=id_number, dsc=dsc, amount=amount, category=category, date=date) # if user is updating a non-existing expense, add that expense (with id greater than settings["last_id"])

        # sort expenses by id number when existing expense was updated
        if settings["last_id"] > id_number:
            with open(f"{self._cur_path}\\Data\\expenses.csv", newline='') as file:
                reader = csv.reader(file)
                columns = next(reader)
                rows = list(reader)

            rows = sorted(rows, key=lambda x: int(x[0]))

            with open(f"{self._cur_path}\\Data\\expenses.csv", 'w', newline='') as file:
                writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(columns)
                writer.writerows(rows)

    def delete(self, self_executed = False, **kwargs):
        # Set variables from kwargs
        id_number = kwargs.get('id_number')
        if id_number is None:
            print("Not all necessery arguments were provided.")
            return

        try:
            id_number = int(id_number)
        except ValueError:
            print("ID must be a number.")
            return

        # Load settings
        try:
            with open(f"{self._cur_path}\\Data\\settings.json") as file:
                settings = json.load(file)

        except FileNotFoundError or json.decoder.JSONDecodeError:
            print(f"No expenses were made yet or the expenses.csv file directory had been changed\nInitial directory ({self._cur_path}\\Data).")
            return

        # Delete
        try:
            df = pandas.read_csv(f"{self._cur_path}\\Data\\expenses.csv", index_col="ID")

            # decrease by 1 the last id number if the last expense is getting deleted
            if id_number == settings["last_id"]:
                self._update_settings(last_id=id_number-1)

            # find row with provided id to decrease sums in settings["amounts"]
            with open(f"{self._cur_path}\\Data\\expenses.csv", newline='') as file:
                reader = list(csv.reader(file))

            start = 1 # in row 0 are column names
            end = len(reader) - 1
            result = 1
            while start <= end:
                mid = int((start + end) / 2)
                if int(reader[mid][0]) <= id_number:
                    start = mid + 1
                    result = mid
                else:
                    end = mid - 1

            # if id wasn't found
            if int(reader[result][0]) != id_number:
                raise KeyError()

            tokens = reader[result][1].split('.')
            self._update_settings(amount=-float(reader[result][4]), year=tokens[2], month=int(tokens[1]), category=reader[result][3])

            df = df.drop(int(id_number))
            df.to_csv(f"{self._cur_path}\\Data\\expenses.csv", index=True)
            if not self_executed:
                print("Expense deleted successfully.")

        except FileNotFoundError:
            if not self_executed:
                print(f"No expenses were made yet or the expenses.csv file directory had been changed\nInitial directory ({self._cur_path}\\Data).")

        except KeyError:
            if not self_executed:
                print("Expense with given ID doesn't exist.")

    def delete_all(self, **kwargs):
        try:
            with open(f"{self._cur_path}\\Data\\expenses.csv") as file:
                reader = csv.reader(file)
                next(reader)

                for row in list(reader):
                    self.delete(self_executed=True, id_number=int(row[0]))
            self._update_settings(last_id=0)

        except FileNotFoundError:
            print(f"expenses.csv file was deleted or moved.\n Initial file directory: ({self._cur_path}\\Data).")

    def enlist(self, **kwargs): # make data table from a csv file
        try:
            with open(f"{self._cur_path}\\Data\\expenses.csv") as file:
                reader = list(csv.reader(file))

            if len(reader) > 1:
                print(pandas.read_csv(f"{self._cur_path}\\Data\\expenses.csv", index_col=0))
            else:
                print("Expenses list is empty.")

        except FileNotFoundError or json.decoder.JSONDecodeError:
            print("No expenses has been added yet, or expenses.csv file directory had been changed\nInitial directory (" + self._cur_path + "\\Data).")

    def summarise(self, **kwargs):
        # Set variables from kwargs
        year = kwargs.get('year')
        month = kwargs.get('month')
        category = kwargs.get('category')

        # Check whether data is entered correctly
        if month is not None:
            try:
                month = int(month)
                if not 1 <= month <= 12:
                    print("Month must be a number between 1 and 12.")
                    return

            except ValueError:
                print("Month must be a number.")
                return

        # Create helper structure
        months = {
            1 : "January", 2 : "Fabuary", 3 : "March", 4 : "April", 5 : "May", 6 : "June", 7 : "July", 8 : "August", 9 : "September", 10 : "October", 11 : "November", 12 : "December"
        }

        # Load settings
        try:
            with open(f"{self._cur_path}\\Data\\settings.json") as file:
                settings = json.load(file)
                amounts = settings["amounts"]

        except FileNotFoundError or json.decoder.JSONDecodeError:
            if year is None: # if no expeses are added, the sums are equal to 0
                print("Total expenses: 0\nNo expenses were added.")

            elif month is None and category is None: # year expenses
                print(f"Total expenses for {year}: 0\nNo expenses were added.")

            elif category is None: # year with specified month
                print(f"Total expenses for {months[month]} {year}: 0\nNo expenses were added.")

            elif month is None: # year with specified category
                print(f"Total expenses for category {category} in {year}: 0\nNo expenses were added.")

            else: # year with specified month and category
                print(f"Total expenses for category {category} in {months[month]} {year}: 0\nNo expenses were added.")
            return

        # check if given arguments exist in caches
        if year is not None:
            try:
                amounts[year]
            except KeyError:
                print("Expenses from provided year were not found.")
                return

        # calculate total amount from caches
        total = float(0)
        if year is None: # if year wasn't spcified
            if category is not None and month is not None: # sum up expenses made in 'month' with category 'category'
                for key in amounts.keys():
                    try:
                        total += amounts[key]["category"][category][month - 1]
                    except KeyError:
                        continue
                print(f"Total expenses for category {category} in {months[month]}: {total}")

            elif category is None: # sum up all expenses made in 'month'
                for key in amounts.keys():
                    total += amounts[key]["month"][month - 1]
                print(f"Total expenses for {months[month]} in each year: {total}")

            elif month is None: # sum up expenses with category 'category'
                for key in amounts.keys():
                    for m in range(12):
                        try:
                            total += amounts[key]["category"][category][m]
                        except KeyError:
                            break
                print(f"Total expenses for category {category}: {total}")

            else: # sum up all expenses if nothing is entered
                for key in amounts.keys():
                    for m in range(12):
                        total += amounts[key]["month"][m]
                print(f"Total expenses: {total}")

        elif month is None and category is None:
            for i in range(12):
                total += amounts[year]["month"][i]
            print(f"Total expenses for {year}: {total}")

        elif month is None:
            for i in range(12):
                total += amounts[year]["category"][category][i]
            print(f"Total expenses for category {category} in {year}: {total}")

        elif category is None:
            total = amounts[year]["month"][month - 1]
            print(f"Total expenses for {months[month]} {year}: {total}")

        else:
            total = amounts[year]["category"][category][month - 1]
            print(f"Total expenses for category {category} in {months[month]} {year}: {total}")

    def set_budget(self, **kwargs):
        # Set variables form kwargs
        budget = kwargs.get('budget')
        year = kwargs.get('year')
        month = kwargs.get('month')

        # Check cases
        if None in (budget, year, month):
            print("Not all necessery arguments were provided.")
            return

        if not os.path.exists(f"{self._cur_path}\\Data\\settings.json"):
            print("At least one expense must be added to set the budget.")
            return

        try:
            budget = float(budget)
            month = int(month)

        except ValueError:
            print("Budget and month must be a number.")
            return

        if not 1 <= month <= 12:
            print("Month must be a number between 1 and 12.")
            return

        if budget < 0:
            print("Budget must be a positive number.")
            return

        # set budget
        try:
            self._update_settings(new_budget=budget, year=year, month=month)
            print(f"Budget for the entered month had been set to: {budget}")
        except KeyError:
            print("At least one expense must be added in the entered year to set the budget.")

    def delete_budget(self, **kwargs): # sets the budget for the secific month and year to default (-1, meaning no budget)
        # Set variables from kwargs
        year = kwargs.get('year')
        month = kwargs.get('month')

        # Check cases
        if None in (year, month):
            print("Not all necessery arguments were provided.")
            return
        if not os.path.exists(f"{self._cur_path}\\Data\\settings.json"):
            print("All budgets are currently set to default.")
            return

        try:
            month = int(month)

        except ValueError:
            print("Month must be a number.")
            return

        if not 1 <= month <= 12:
            print("Month must be a number between 1 and 12.")
            return

        # delete budget
        try:
            self._update_settings(year=year, month=month, new_budget=-1)
            print("Budget for the entered month had been deleted.")
        except KeyError:
            print("Entered year has no expenses.")

    def _set_date(self, date):
        if len(date) != 10: # dd.mm.yyyy form of a date contains 10 symbols
            print("Inproper date format (not dd.mm.yyyy).\nDate has been set to today's.")

        else:
            for i in range(10):
                if i in (2, 5) and i != '.': # if dots are on their places
                    print("Day, month and year must be separated with a dot.\nDate has been set to today's.")
                    return

            temp = date.split('.')
            try:
                if not (1 <= int(temp[0]) <= 31 and 1 <= int(temp[1]) <= 12 and 1000 <= int(temp[2]) <= 9999):
                    print("Day, month or year are out of bounds.\nDate has been set to today's.")
                else:
                    if temp[0] == "31" and temp[1] not in ("01", "03", "05", "07", "08", "10", "12"):
                        print("Unmatchable day and month.\nDate has been set to today's.")

                    elif temp[0] == "30" and temp[1] not in ("04", "06", "09", "11"):
                        print("Unmatchable day and month.\nDate has been set to today's.")

                    elif int(temp[0]) > 29 and temp[1] == "02":
                        print("Unmatchable day and month.\nDate has been set to today's.")

                    else:
                        self._dt = date
            except ValueError:
                print("Day, month or year aren't numeric or are inproper.\nDate has been set to today's.")

    # change settings.json based on provided arguments
    def _update_settings(self, year=None, month=None, new_budget=None, last_id=None, category=None, amount=float(0)):
        # eventual errors are handled inside other methods
        # user can not run this method, becouse argpare in main file doesn't recognize it
        with open(f"{self._cur_path}\\Data\\settings.json") as file:
            settings = json.load(file)

        if new_budget is not None: # setting or deleting the budget
            settings["budget"][year][month - 1] = float(new_budget)

        if last_id is not None: # updating latest added id
            settings["last_id"] = last_id

        if category is not None: # adding, updating or deleting
            settings["amounts"][year]["month"][month - 1] += amount # update amounts at "month"
            try: # update amounts at "category"
                settings["amounts"][year]["category"][category][month - 1] += amount

            except KeyError: # in case list of months for given category wasn't created
                settings["amounts"][year]["category"][category] = [float(0) for i in range(12)]
                settings["amounts"][year]["category"][category][month - 1] += amount

        with open(f"{self._cur_path}\\Data\\settings.json", 'w') as file:
            file.write(json.dumps(settings))