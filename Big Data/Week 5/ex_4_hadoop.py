def 十(*args):
    return sum(args)

def 一(a, *args):
    return a - sum(args)

def 乛(*args):
    result = args[-1]  # Start from the last element
    for num in reversed(args[:-1]):  # Iterate in reverse order, skipping the last element
        result = num - result  # Right-associative subtraction
    return result

def ϵ(tree):
    result = []
    for item in tree:
        if isinstance(item, list):
            result.extend(ϵ(item))  # Recursively flatten nested lists
        else:
            result.append(item)  # Append non-list elements directly
    return result

def γ(f, seq):
    result = {}
    for item in seq:
        key = f(item)  # Apply function to get the key
        if key not in result:
            result[key] = []  # Initialize list if key doesn't exist
        result[key].append(item)  # Append item to the corresponding list
    return result


