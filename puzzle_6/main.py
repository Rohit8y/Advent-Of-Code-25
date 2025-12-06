import numpy as np
import pandas as pd
import ast
import operator

# allowed operators
ops = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg
}


def safe_eval(expr):
    def _eval(node):
        if isinstance(node, ast.Num):  # number
            return node.n
        if isinstance(node, ast.BinOp):  # binary operation
            return ops[type(node.op)](_eval(node.left), _eval(node.right))
        if isinstance(node, ast.UnaryOp):  # unary (negative numbers)
            return ops[type(node.op)](_eval(node.operand))
        raise TypeError("Unsupported expression")

    node = ast.parse(expr, mode='eval')
    return _eval(node.body)


def get_input_data(file_path="sample_input.txt"):
    return pd.read_csv(file_path, delim_whitespace=True, header=None)


def get_input_data_with_formatting(file_path="sample_input.txt"):
    # Read the file as a list of lines (preserve spaces)
    with open(file_path, "r") as f:
        lines = [line.rstrip("\n") for line in f]

    # Transpose the grid: get each column as a string of characters
    num_cols = max(len(line) for line in lines)
    grid = [line.ljust(num_cols) for line in lines]  # pad short lines
    columns = []
    for col_idx in range(num_cols):
        col = "".join(grid[row_idx][col_idx] for row_idx in range(len(lines)))
        columns.append(col)
    return columns


def solve_part1(df):
    final_output = 0
    for col in df.columns:  # col will be 0, 1, 2, 3, ...
        operator = df[col].to_list()[-1]
        data = df[col].to_list()[:-1]
        expression = ""
        for number in data:
            expression = expression + number + operator

        # Remove last operator
        expression = expression[0:-1]

        output = safe_eval(expression)
        final_output += output

    print("Output: ", final_output)
    return final_output


def convert_right_to_left(sequence):
    print("Input:", sequence)
    df_cephalopod = None
    for number in sequence:
        array_integers = []
        for number_char in number:
            array_integers.append(int(number_char))

        # Update dataframe
        if df_cephalopod is None:
            df_cephalopod = pd.DataFrame([array_integers])
        else:
            df_cephalopod = pd.concat(
                [df_cephalopod, pd.DataFrame([array_integers])],
                ignore_index=True
            )

    # Shift everything right
    def right_align(row):
        vals = row.dropna().tolist()  # keep non-NaNs in order
        n = len(row)
        k = len(vals)
        return pd.Series([np.nan] * (n - k) + vals, index=row.index)

    df_cephalopod = df_cephalopod.apply(right_align, axis=1)

    # Get numbers in cephalopod format starting from last column
    input_numbers_cephalopod = []
    for col_idx in range(len(df_cephalopod.columns) - 1, -1, -1):
        number_cephalopod = ""
        for value in df_cephalopod[col_idx]:
            if not pd.isna(value):
                number_cephalopod = number_cephalopod + str(int(value))
        input_numbers_cephalopod.append(number_cephalopod)

    print(input_numbers_cephalopod)
    print(df_cephalopod)
    return input_numbers_cephalopod


def parse_problems(columns):
    problems = []
    current_problem = []

    for col in columns:
        # If the column is entirely spaces, it separates problems
        if col.strip() == "":
            if current_problem:
                problems.append(current_problem)
                current_problem = []
        else:
            current_problem.append(col)

    if current_problem:
        problems.append(current_problem)

    # Cephalopod math: problems are read right-to-left
    problems = problems[::-1]
    return problems


def evaluate_problem(problem_cols):
    # Last row of each column contains the operator (bottom char)
    operator = problem_cols[0][-1]

    numbers = []
    for col in problem_cols:
        # Extract all digits except the last character (operator)
        digits = col[:-1].rstrip()  # remove trailing spaces
        # Convert to integer
        number = int(digits)
        numbers.append(number)

    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        result = 1
        for n in numbers:
            result *= n
        return result
    else:
        raise ValueError(f"Unknown operator {operator}")


def solve_part2(columns):
    problems = parse_problems(columns)

    results = []
    for problem in problems:
        res = evaluate_problem(problem)
        results.append(res)

    grand_total = sum(results)

    print("Problem results (right-to-left):", results)
    print("Grand total:", grand_total)


def main():
    file_path = "input.txt"

    print("-----------Solving Part 1")
    # Part 1
    df = get_input_data(file_path)
    solve_part1(df)

    print("-----------Solving Part 2")
    # Part 2
    columns = get_input_data_with_formatting(file_path)
    solve_part2(columns)


if __name__ == '__main__':
    main()
