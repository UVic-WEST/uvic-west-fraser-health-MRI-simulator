# Docstring Template
## Instructions:

Under every function (including class \__init__() functions), use this template to document the functionality of the function.

IMPORTANT NOTE!
if a function has no arguments or has no returns, just remove that section entirely to save space, but a description should always be completed. There is an example of usage bellow as well.

## Template:
```Python 
"""
*Function description, what does this function do yada yada/ any 
relevant information that may be necessary without divulging 
full implementation logic*

Args:
	arg_name (type): *what this argument is meant to represent*
	arg2_name (type): *what this argument is meant to represent*

Returns:
	(type): *what this return value represents*
"""
```
### Example usage:

WITH arguments and returns

```Python
def return_cycle_duration (self, cycle_id:int) -> int:
	"""
	This function returns the duration (in milliseconds) of a specified cycle by using it's id.

	Args:
		cycle_id (int): the id of the cycle to find the duration of

	Returns:
		(int): the duration of the specified cycle in milliseconds
	"""
```

WITHOUT arguments and returns. Note that if there were say arguments but no returns you would keep the arguments section and just fully remove the return section.

```Python
def __init__ (self):
	"""
	This is for the XX class and this is what it does
	"""
```