from fastapi.concurrency import run_in_threadpool
from sympy import sympify, SympifyError


async def solve_math_problem(expression: str) -> str | None:
    """
    Solves a mathematical expression using Sympy.
    Returns the result as a string, or None if the expression is invalid.
    This fulfills the "Accuracy First" principle.
    """
    def _solve():
        try:
            # Use sympify to safely evaluate the string expression
            solution = sympify(expression)
            return str(solution.evalf())
        except (SympifyError, TypeError, SyntaxError):
            # The expression was not a valid mathematical one
            return None
    return await run_in_threadpool(_solve)