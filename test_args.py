# --- file test_args.py ---

# import friendly_arguments
from friendly_arguments.named import get_params_sys_args

# Make a function call, passing as an argument a list of strings,
# with the prefix '-' or '--' and the suffix '='. example '--arg1=' or '-arg1='
my_args: dict = get_params_sys_args(['--text='])

# validate the arguments
try:
    text1 = my_args['--text=']
except KeyError:
    raise ValueError('argumets --text= empty')

print(text1)