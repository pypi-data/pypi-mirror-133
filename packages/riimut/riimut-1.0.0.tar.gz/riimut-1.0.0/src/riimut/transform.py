def transform(content: str, mapping: "dict[str, str]") -> str:
    result = ""

    for letter in content:
        result += mapping.get(letter.lower(), letter)

    return result
