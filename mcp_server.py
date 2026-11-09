from mcp.server import MCPServer
from datetime import datetime
import ast
import operator

mcp = MCPServer("venkat-tools")

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("unsupported expression")

@mcp.tool()
def word_count(text: str) -> int:
    """Count the words in the given text."""
    return len(text.split())

@mcp.tool()
def get_current_time() -> str:
    """Returns the current local date and time. Call this for any question about the current time or date. Takes no arguments, pass {}."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool()
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression like '240*0.15' or '(9*3)+2'.
    Supports +, -, *, /, ** and parentheses. No percentages, no words."""
    try:
        return str(_eval(ast.parse(expression, mode="eval")))
    except Exception as e:
        return f"Error: {e}"

@mcp.resource("venkat://calculator-rules", mime_type="text/plain")
def calculator_rules() -> str:
    """What the calculator accepts."""
    return "Digits, + - * / **, parentheses, decimals. No percent phrasing like '15% of 240' — use 0.15 * 240."

_DOCS = {
    "calculator": calculator.__doc__,
    "word_count": word_count.__doc__,
    "get_current_time": get_current_time.__doc__,
}

@mcp.resource("venkat://tool/{name}")
def tool_doc(name: str) -> str:
    """Description of one tool, by name."""
    return _DOCS.get(name, "unknown tool")

@mcp.prompt()
def fox_times_three(multiplier: str = "3") -> str:
    """Count the fox-sentence words and multiply."""
    return f"Count the words in 'the quick brown fox jumps over the lazy dog' and multiply by {multiplier}."


if __name__ == "__main__":
    #mcp.run(transport="stdio")
    mcp.run(transport="streamable-http", port=8000)

