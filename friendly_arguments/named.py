import sys
from typing import Dict


def get_params_sys_args(keys: list) -> Dict[str, str]:
    """
    example run:\n
    '''python my_script --arg_1=value_thing1 --arg_2=value_thing2'''\n
    example code:\n
    my_args = get_params_sys_args(['--arg_1=', '--arg_2='])\n
    arg1 = my_args.get('--arg_1=') # value_thing1\n
    arg2 = my_args.get('--arg_2=') # value_thing2\n
    arg3 = my_args.get('--arg_3=') # None\n
    :param keys:  ["--paramkey=", "-p="] add "--name_params=" or "-name_params="
    :return:
    """
    args_dict = {}
    for i in range(1, len(sys.argv)):
        for key in keys:
            if sys.argv[i].find(key) == 0:
                print(f"The {key} value is: {sys.argv[i][len(key):]}")
                args_dict[key] = sys.argv[i][len(key):]
                break
    return args_dict