
#### Install from pip

~~~ shel 
linux: pip3 install cli-args-system
windows: pip install cli-args-system
~~~
#### Install from scratch
#
~~~ shel 
linux: sudo python3 setup.py install
windows: python setup.py install
~~~
#
#


## What is cli_args_system ?
In an general way its a library to manipulate argv args its content and its flags 
#
#


## Basic Usage 
###### the most basic application:
#
~~~~ python
from cli_args_system import Args

args = Args()
print(args)
~~~~
###### running:
~~~~ shel 
$ python3  test.py  -a "value of a" -b "value of b"
~~~~
###### results:
#
~~~ json
{
    "default": [],
    "a": [
        "value of a "
    ],
    "b": [
        "value of b"
    ]
}
~~~
#
#

### Args:
###### retrieving the args: 
#
~~~~python
from cli_args_system import Args

args = Args()

list_of_args = args.args()
print(list_of_args)
~~~~

###### accessing args index:
#
~~~~python
from cli_args_system import Args

args = Args()

try:
    print(f'second arg is {args[1]}')
except IndexError:
    print('there less than 2 args')


~~~~
###### making iterations:
#
~~~~python
from cli_args_system import Args

args = Args()

for a in args:
    print(a)
~~~~


### Flags:

###### retrieving all flags dict:
#
~~~ python
from cli_args_system import Args

args = Args()

flags = args.flags_dict()
print(flags)
~~~
###### running:
#
~~~ shell
 python3 test.py 0 0x   -a 10 1a -b 20 1b 
 -> {'default': [0, '0x'], 'a': ['10', '1a'], 'b': [20, '1b']}
~~~
###### getting FlagsContent Object:
#
~~~ python
from cli_args_system import Args

args = Args()
out = args.flags_content('o','out')
print(out)
~~~
###### running:
#
~~~ shell
python3 test.py -o a.txt
 -> 
exist:  True
filled: True
args:   ['a.txt']
~~~

###### retrieving  flags and making iterations:
#
~~~ python
from cli_args_system import Args

args = Args()
out = args.flags_content('o','out')

full_list = out.flags()

try:
    first_element = out[0]
    print(f'first element is: {first_element}')
except IndexError:pass 

#making iterations
for f in out:
    print(f)

print(f'full list is: {full_list}')
~~~
###### running:
#
~~~ shell
python3 test.py -o a.txt b.txt
 -> 
first element is: a.txt
a.txt
b.txt
full list is: ['a.txt', 'b.txt']
~~~
###### checking Flags Status:
#
~~~ python
from cli_args_system import Args

args = Args()
out = args.flags_content('o','out')

if out.exist():
    print('out flag exist')

if out.exist_and_empty():
    print('out flag exist but its empty')

if out.filled():
    print('out flag its filled')

if 'a.txt' in out:
    print('a.txt in out flag')
~~~
###### running:
#
~~~ shell
python3 test.py -o a.txt
->
out flag exist
out flag its filled
a.txt in out flag
~~~


