from typing import Optional, Any
from sympy import sympify, SympifyError
from fastapi.concurrency import run_in_threadpool
from .base import BaseTool

class MathSolverTool(BaseTool):
    """Tool for solving mathematical expressions."""

    def get_name(self) -> str:
        return "math_solver"

    def get_description(self) -> str:
        return "Solves mathematical expressions using the Sympy library."

    async def execute(self, expression: str = None, **kwargs) -> Optional[str]:
        if not expression:
            return None
            
        def _solve():
            try:
                # Use sympify to safely evaluate the string expression
                solution = sympify(expression)
                return str(solution.evalf())
            except (SympifyError, TypeError, SyntaxError):
                # The expression was not a valid mathematical one
                return None

        return await run_in_threadpool(_solve)
