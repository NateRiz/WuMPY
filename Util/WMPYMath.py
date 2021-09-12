def clamp(min_, max_, x):
    return max(min(max_, x), min_)

def try_parse_color(color):
    sanitized = "".join([i for i in color if i.isdigit() or i == ","])
    parsed = sanitized.split(",")
    if len(parsed) == 3 and all([i.isdigit() for i in parsed]):
        return [clamp(0, 255, int(i)) for i in parsed]

    return [0, 0, 0]