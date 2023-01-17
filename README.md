# FriendlyArguments

This python package makes it easy to use command line argument

## Install
```pip install friendly-arguments``` 

## Example

**CODE** file: test_args.py 
````python
# import friendly_arguments
from friendly_arguments.named import get_params_sys_args

# Make a function call, passing as an argument a list of strings, 
# with the prefix '-' or '--' and the suffix '='. example '--arg1=' or '-arg1='
my_args: dict = get_params_sys_args(['--text='])

# validate your arguments as you wish
try:
    text1 = my_args['--text=']
except KeyError:
    raise ValueError('argumets --text= empty')

print(text1)

# OR

text1 = my_args.get('--text=')
if text1 is None:
    raise ValueError('argumets --text= empty')

````
 
**RUN** on terminal
```shell
python test_args.py --text=hello_world
# or 
python test_args.py --text="hello world"
```




