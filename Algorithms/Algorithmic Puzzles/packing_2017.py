
def pack_items(items):
    # The sorted function returns a sorted list from an iterable,
    # and an optional key that serves as the sort comparison:
    # This key indicates that for each item in the items iterable, sum "s" and "w", using this as the value for sorting:
    return sorted(items, key=lambda item: item.get("s") + item.get("w"))


if __name__ == "__main__":
    test_items = [
        {"name": "Apples", "w": 5, "s": 6},
        {"name": "Bread", "w": 4, "s": 4},
        {"name": "Carrots", "w": 12, "s": 9}
    ]

    print(pack_items(test_items))
