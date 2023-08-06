"""
Math problem generator. Needs python 3.8 or higher.
"""
import operator
import random

from typing import List, TypedDict, Union


class SimpleMathProblem(TypedDict):
    type: str
    operator: str
    numbers: List[Union[int, float]]
    solution: Union[None, int, float]
    users_answer: Union[None, int, float]


def simple_solution(operator_name: str, numbers: List[int]) -> Union[None, int, float]:
    """
    Calculate the solution for a list of numbers and an operator
    """

    if len(numbers) < 2:
        raise ValueError("Numbers list too short")

    # Define the operator function to use
    if operator_name == "add":
        o = operator.add
    elif operator_name == "sub":
        o = operator.sub
    elif operator_name == "mul":
        o = operator.mul
    elif operator_name == "div":
        o = operator.truediv
    else:
        raise ValueError(f"Invalid operator: '{operator_name}'")

    # Calculate result
    r = numbers[0]
    for n in numbers[1:]:
        try:
            r = o(r, n)
        except ZeroDivisionError:
            return None

    return r


def simple_problems(
    op: str,
    no_of_problems: int = 25,
    min_number: int = 1,
    max_number: int = 100,
    numbers: int = 2,
    seed: Union[None, str] = None,
    decimals: int = 4,
    sort_numbers: bool = False,
) -> List[SimpleMathProblem]:
    """
    Generate simple math problems like 1+2=3
    """

    # Can't generate problems with less than 2 numbers
    if numbers < 2:
        raise ValueError("Argument 'numbers' less that 2")

    # Supply sees for predictable problems
    if seed:
        random.seed(seed)

    problem_list = []

    # Generate the problems
    for i in range(no_of_problems):
        # Empty problem dict
        p: SimpleMathProblem = {
            "type": "simple",
            "operator": op,
            "numbers": [],
            "solution": None,
            "users_answer": None,
        }

        # Generate numbers for problem
        for i in range(numbers):
            p["numbers"].append(random.randint(min_number, max_number))

        # Sort highest numbers first
        if sort_numbers:
            p["numbers"].sort(reverse=True)

        # Add the result to the problem
        p["solution"] = simple_solution(op, p["numbers"])

        # Add problem to list of problems
        problem_list.append(p)

    return problem_list
