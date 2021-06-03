def AND(first, second):
    return f"({first} AND {second})"


def OR(first, second):
    return f"({first} OR {second})"


def EQUAL(field, value):
    return f"{field} = {value}"


def LESS(field, value):
    return f"{field} < {value}"


def LESS_OR_EQUAL(field, value):
    return f"{field} <= {value}"


def GREATER(field, value):
    return f"{field} > {value}"


def GREATER_OR_EQUAL(field, value):
    return f"{field} >= {value}"


def IS_NULL(field):
    return f"{field} IS NULL"


def LIKE(field, pattern):
    return f"{field} LIKE '{pattern}'"


def IN(field, values_or_query):
    if isinstance(values_or_query, str):
        formatted_values = values_or_query
    else:
        formatted_values = ", ".join(map(str, values_or_query))

    return f"{field} IN ({formatted_values})"
