def sanitize_name(name: str) -> str:
    lookup_table = {
        0: "=",
        2: "=",
        5: "•",
        10: " ",
        14: "•",
        15: "•",
        16: "[",
        17: "]",
        18: "0",
        19: "1",
        20: "2",
        21: "3",
        22: "4",
        23: "5",
        24: "6",
        25: "7",
        26: "8",
        27: "9",
        28: "•",
        29: "=",
        30: "=",
        31: "="
    }
    return "".join(
        map(
            lambda c: chr(c) if c >= 32 else lookup_table.get(c, '?'),
            map(
                lambda c: c if c < 128 else c - 128,
                map(ord, name)
            )
        )
    ).replace("'", "")
