from enum import Enum
def report_error(line, message):
    print(f"Line {line}: {message}")

class TokenType(Enum):
    LEFT_BRACKET = 1
    RIGHT_BRACKET = 2
    LEFT_CURL = 3
    RIGHT_CURL = 4
    COMMA = 5
    DOT = 6
    MINUS = 7
    PLUS = 8
    SEMICOLON = 9
    SLASH = 10
    STAR = 11

    EXCLAM = 12
    NEQ = 13
    ASSIGN = 14
    EQ = 15
    GT = 16
    GEQ = 17
    LT = 18
    LEQ = 19

    IDENTIFIER = 20
    STRING = 21
    NUMBER = 22

    AND = 23
    CLASS = 24
    ELSE = 25
    FALSE = 26
    FUN = 27
    FOR = 28
    IF = 29
    NIL = 30
    OR = 31
    PRINT = 32
    RETURN = 33
    SUPER = 34
    THIS = 35
    TRUE = 36
    VAR = 37
    WHILE = 38

    EOF = 39

class Token:
    def __init__(self, type, lexeme, line, literal=None, ):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    def __repr__(self) -> str:
        return f"type:{self.type} lexeme:{self.lexeme} literal:{self.literal} line:{self.line}"

def scan_tokens(source):
    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }
    
    tokens = []
    current = 0
    line = 1
    start = 0
    def check_next(expected):
        nonlocal current
        if source[current] != expected or current >= len(source):
            return False
        else:
            current += 1
            return True
    def peek_next():
        if current >= len(source):
            return "\0"
        else:
            return source[current]
    def peek_twice():
        
        if current+1 >= len(source):
            return "\0"
        else:
            return source[current+1]
    while current < len(source):
        start = current
        c = source[current]
        current += 1
        match c:
            case "(":
                tokens.append(Token(
                    type=TokenType.LEFT_BRACKET,
                    lexeme=source[start:current],
                    line=line
                ))
            case ")":
                tokens.append(Token(
                    type=TokenType.RIGHT_BRACKET,
                    lexeme=source[start:current],
                    line=line
                ))
            case "{":
                tokens.append(Token(
                    type=TokenType.LEFT_CURL,
                    lexeme=source[start:current],
                    line=line
                ))
            case "}":
                tokens.append(Token(
                    type=TokenType.RIGHT_CURL,
                    lexeme=source[start:current],
                    line=line
                ))
            case ",":
                tokens.append(Token(
                    type=TokenType.COMMA,
                    lexeme=source[start:current],
                    line=line
                ))
            case ".":
                tokens.append(Token(
                    type=TokenType.DOT,
                    lexeme=source[start:current],
                    line=line
                ))
            case "-":
                tokens.append(Token(
                    type=TokenType.MINUS,
                    lexeme=source[start:current],
                    line=line
                ))
            case "+":
                tokens.append(Token(
                    type=TokenType.PLUS,
                    lexeme=source[start:current],
                    line=line
                ))
            case ";":
                tokens.append(Token(
                    type=TokenType.SEMICOLON,
                    lexeme=source[start:current],
                    line=line
                ))
            case "*":
                tokens.append(Token(
                    type=TokenType.STAR,
                    lexeme=source[start:current],
                    line=line
                ))
            
            case "!":
                token_type = TokenType.NEQ if check_next("=") else TokenType.EXCLAM
                tokens.append(Token(
                    type=token_type,
                    lexeme=source[start:current],
                    line=line
                ))
            case "=":
                token_type = TokenType.EQ if check_next("=") else TokenType.ASSIGN
                tokens.append(Token(
                    type=token_type,
                    lexeme=source[start:current],
                    line=line
                ))
            case "<":
                token_type = TokenType.LEQ if check_next("=") else TokenType.LT
                tokens.append(Token(
                    type=token_type,
                    lexeme=source[start:current],
                    line=line
                ))
            case ">":
                token_type = TokenType.GEQ if check_next("=") else TokenType.GT
                tokens.append(Token(
                    type=token_type,
                    lexeme=source[start:current],
                    line=line
                ))

            case "/":
                is_comment = check_next("/")
                if is_comment:
                    while peek_next() != "\n" and current < len(source):
                        current += 1
                else:
                    tokens.append(Token(
                    type=TokenType.SLASH,
                    lexeme=source[start:current],
                    line=line
                ))
                    
            case " " | "\r" | "\t":
                pass
            case "\n":
                line += 1
            case "\"":
                while peek_next() != "\"" and current < len(source):
                    if peek_next() == "zn":
                        line += 1
                    current += 1
                if current >= len(source):
                    report_error(line, "Unterminated string")
                current += 1
                value = source[start+1:current-1]
                tokens.append(Token(
                    type=TokenType.STRING,
                    lexeme=source[start:current+1],
                    line=line,
                    literal=value
                ))
            
            case _:
                if c.isdigit():
                    while peek_next().isdigit():
                        current += 1
                    if peek_next() == "." and peek_twice().isdigit():
                        current += 1
                    while peek_next().isdigit():
                        current += 1
                    tokens.append(Token(
                        type=TokenType.NUMBER,
                        lexeme=source[start:current],
                        line=line,
                        literal=source[start:current]
                    ))
                elif c.isalpha():
                    while peek_next().isalnum():
                        current += 1
                    text = source[start:current]
                    token_type = keywords.get(text)
                    if token_type == None:
                        tokens.append(Token(
                            type=TokenType.IDENTIFIER,
                            lexeme=text,
                            line=line,
                            literal=text
                        ))
                    else:
                        tokens.append(Token(
                            type=token_type,
                            lexeme=text,
                            line=line,
                            literal=text
                        ))

                    
    return tokens