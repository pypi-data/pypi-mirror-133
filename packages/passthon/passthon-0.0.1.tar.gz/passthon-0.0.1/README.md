
# passthon

passthon is a Python library for easily generating random passwords.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install passthon.

```bash
pip install passthon
```

## Usage

First, you need to import the library into your script.

```python
import passthon
```

### The password class
The password class is the main (and the only) class in the passthon module. You will need to directly instantiate it in order to generate passwords.

```python
mypassword = passthon.password(length[,options])
```

**Parameters:**
| Name | Type | Description | Default |
|:---:|:---:|:---:|:---:|
| ***length*** | int  | The length of the password(s) you want to generate.  | Doesn't have a default value. You need to specify the length.
| ***lc*** | bool  | Include lowercase letters.|Defaults to `True`
| ***uc*** | bool  | Include uppercase letters.|Defaults to `False`
| ***num*** | bool  | Include numbers.|Defaults to `True`
| ***sym*** | bool  | Include lowercase characters.|Defaults to `False`

**Example:**
This example corresponds to a 10-character password with only uppercase letters and numbers.  
Remember that **lc** and **num** parameters are True by default.
```python
mypassword = passthon.password(10, lc=False, uc=True)
```

### Functions
#### The gen() function
To generate a password based on the previous parameters, you will need to call the gen() function on the instance you previously created.  
```python
mypassword.gen()
# This will return a randomly generated password.
```

#### The gen_multi() function
Similar to the gen() function, but this one generates more than one password. You will need to specify the amount of passwords you want to generate.
```python
mypassword.gen_multi(amount)
# This will return a certain amount of passwords as a list.
```
As this function returns a *list*, you can access each one of the passwords through their index, or even join them in a single *string*.

**Example:**
```python
list = mypassword.gen_multi(10)
print(list[3])
# This will print password 4 of 10

string = '-'.join(list)
print(string)
# This will print all 10 passwords separated by a dash (-)
```

#### The print() function
This function will directly print a previously generated password. If there's no password generated, it will automatically generate one and print it.

When used in a multi-password context, it prints the list one by one.
```python
mypassword.print()
```

## Contributing
Pull requests are welcome. Also, if you find any problem or error, feel free to contact me. :D


## License
[MIT](https://choosealicense.com/licenses/mit/)