try:
    from cli_app_tools.functionalities import Tracker
except ImportError:
    import os
    print("Functionalities module has been moved or deleted.\nInitial directory: " + os.getcwd() + "\\cli_app_tools")
    exit(0)
import argparse

f = Tracker()
avaliable_functions = {
    "add" : f.add,
    "update" : f.update,
    "delete" : f.delete,
    "delete_all" : f.delete_all,
    "enlist" : f.enlist,
    "summarise" : f.summarise,
    "set_budget" : f.set_budget,
    "delete_budget" : f.delete_budget
}

parser = argparse.ArgumentParser()
parser.add_argument("function")
args, unknown_args = parser.parse_known_args()

dashed_parser = argparse.ArgumentParser()

for argument in ("--description", "--category", "--amount", "--id", "--budget", "--year", "--month", "--date"):
    dashed_parser.add_argument(argument, required=False)

dashed_parser = dashed_parser.parse_args(unknown_args)

try:
    avaliable_functions[args.function](dsc=dashed_parser.description,
                                        category=dashed_parser.category,
                                        amount=dashed_parser.amount,
                                        id_number=dashed_parser.id,
                                        budget=dashed_parser.budget,
                                        year=dashed_parser.year,
                                        month=dashed_parser.month,
                                        date=dashed_parser.date)
except KeyError:
    print("Given method could not be found.")