def reflect_vert(custom_charecter: dict[str]):
    return custom_charecter[::-1]


def reflect_hor(custom_charecter: dict[str]):
    return list(map(lambda x: x[::-1], custom_charecter))
