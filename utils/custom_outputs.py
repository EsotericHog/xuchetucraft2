INFORMATION : str = "[INFO]"
WARNING : str = "[WARN]"
ERROR : str = "[ERR]"
SUCCESS : str = "[DONE]"

def print_info(output : str = "Information output"):
    print(f'{INFORMATION} {output}')

def print_warn(output : str = "Warning output"):
    print(f'{WARNING} {output}')

def print_err(output : str = "Error output"):
    print(f'{ERROR} {output}')

def print_done(output : str = "Success output"):
    print(f'{SUCCESS} {output}')