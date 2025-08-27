import re

patterns = [
    [r"print", "print"],
    [r"\d*\.\d+|\d+\.\d*|\d+","number"], #\d = digit, + means one or more, * means 0 or more
    [r"[a-zA-z_][a-zA-Z0-9_]*", "identifier"], # Indentifiers
    [r"\+", "+"],
    [r"\-", "-"],
    [r"\*", "*"],
    [r"\/", "/"],
    [r"\(", "("],
    [r"\)", ")"],
    [r"\s+", "whitespace"],
    [r".", "error"]
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

def tokenize(characters): 
    tokens = []
    position = 0
    while position < len(characters):
        #find first matching token
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break

        assert match

        if tag == "error":
            raise Exception(f"Syntax Error: illegal character : {[match.group(0)]}")

        token = {"tag":tag, "position":position}
        value = match.group(0)
        if token["tag"] == "number":
            if "." in value:
                token["value"] = float(value)
            else:
                token["value"] = int(value)

        if token["tag"] == "identifier":
            token["value"] = value

        if token["tag"] != "whitespace":
            tokens.append(token)
        position = match.end()

    tokens.append({"tag":None, "position":position})
    return tokens

def test_simple_tokens():
    print("test simple tokens")

    for c in "+-*/()":
        assert tokenize(c) == [
            {"tag":c, "position":0},
            {"tag":None, "position":1}
        ]

    assert tokenize("3") == [
        {"tag":"number", "position":0, "value": 3},
        {"tag":None, "position":1}
    ]

    assert tokenize("cat") == [
        {"tag":"identifier", "position":0, "value": "cat"},
        {"tag":None, "position":3}
    ]

def test_simple_expressions():
    print("test simple expressions")
    t = tokenize("2+3")
    assert t == [{'tag': 'number', 'position': 0, 'value': 2}, {'tag': '+', 'position': 1}, {'tag': 'number', 'position': 2, 'value': 3}, {'tag': None, 'position': 3}]

def test_whitespace():
    print("test simple expressions")
    t = tokenize("1 + 2")
    assert t == [{'tag': 'number', 'position': 0, 'value': 1}, {'tag': '+', 'position': 2}, {'tag': 'number', 'position': 4, 'value': 2}, {'tag': None, 'position': 5}]

if __name__ == "__main__":
    print("testing tokenizer")
    test_simple_tokens()
    test_simple_expressions()
    test_whitespace()
    print("done")
