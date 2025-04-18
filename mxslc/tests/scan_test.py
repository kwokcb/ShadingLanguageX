from mxslc.Keyword import FLOAT, STRING
from mxslc.token_types import EOF, IDENTIFIER, FLOAT_LITERAL, INT_LITERAL, STRING_LITERAL
from mxslc.scan import scan


def test_scan_correctly_updates_line_number():
    code = """
        float x = 0.0;
        float y = 0.0;
        float z = 0.0;
    """

    tokens = scan(code)
    assert len(tokens) == 16
    assert tokens[ 0].line == 2
    assert tokens[ 5].line == 3
    assert tokens[10].line == 4


def test_scan_correctly_identifies_tokens():
    tokens = scan("")
    assert tokens[0] == EOF

    tokens = scan("float f = 0.7;")
    assert tokens[0] == FLOAT
    assert tokens[1] == IDENTIFIER
    assert tokens[2] == "="
    assert tokens[3] == FLOAT_LITERAL
    assert tokens[3].value == 0.7
    assert tokens[4] == ";"
    assert tokens[5] == EOF

    tokens = scan("float f = a + 0.5;")
    assert tokens[0] == FLOAT
    assert tokens[1] == IDENTIFIER
    assert tokens[2] == "="
    assert tokens[3] == IDENTIFIER
    assert tokens[4] == "+"
    assert tokens[5] == FLOAT_LITERAL
    assert tokens[5].value == 0.5
    assert tokens[6] == ";"
    assert tokens[7] == EOF

    tokens = scan("i += 3;")
    assert tokens[0] == IDENTIFIER
    assert tokens[1] == "+="
    assert tokens[2] == INT_LITERAL
    assert tokens[2].value == 3
    assert tokens[3] == ";"
    assert tokens[4] == EOF

    tokens = scan('string msg="hello world";')
    assert tokens[0] == STRING
    assert tokens[1] == IDENTIFIER
    assert tokens[2] == "="
    assert tokens[3] == STRING_LITERAL
    assert tokens[3].value == "hello world"
    assert tokens[4] == ";"
    assert tokens[5] == EOF
