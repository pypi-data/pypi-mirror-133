def allkeys(d: dict) -> list:
    """ネストした要素も含めたdict.keys

    Args:
        d (dict): dict

    Returns:
        list: keys

    Example:
        >>> d = {'name': {'first': 'John', 'last': 'Smith'}, 'age': 36}
        >>> allkeys(d)
        ['name.first', 'name.last', 'age']

    Note:
        https://qiita.com/ainn_lll/items/e898b7bc8bfc4afdb445
    """
    keys = []
    for parent, children in d.items():
        if isinstance(children, dict):
            keys += [parent + "." + child for child in allkeys(children)]
        else:
            keys.append(parent)
    return keys
