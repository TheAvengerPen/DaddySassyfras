import datetime

log_file_location = "..\\..\\logs.txt"


def log_error(errormsg):
    with open(log_file_location, "a") as f:
        f.write(f"{datetime.datetime.now().__str__()} --- {errormsg}\n\n")
