def avg_float(float_list: list[float]) -> float:
    """
    Calculate the average of a list of floats.
    """
    return sum(float_list) / len(float_list)


def avg_float_from_tuple_list(
    tuple_list: list[tuple[float, float, float, float]]
) -> tuple[float, float, float, float]:
    """
    Calculate the average of a list of tuples of floats.
    """
    return (
        sum([t[0] for t in tuple_list]) / len(tuple_list),
        sum([t[1] for t in tuple_list]) / len(tuple_list),
        sum([t[2] for t in tuple_list]) / len(tuple_list),
        sum([t[3] for t in tuple_list]) / len(tuple_list),
    )
