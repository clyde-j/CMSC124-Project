import sys
from Scanner import Scanner
from Parser import Parser
from Evaluator import Evaluator


def evaluate_and_print(statement):
    try:
        scanner = Scanner(statement)
        tokens = scanner.get_tokens()

        parser = Parser(tokens)
        parse_tree = parser.parse_sentence()

        variables = [var for var in {"P", "Q", "S"} if var in tokens]
        evaluator = Evaluator(parse_tree)
        truth_table, columns = evaluator.generate_truth_table(variables)

        # Determine column widths for pretty printing
        col_widths = {col: max(len(col), 5) for col in columns}
        for row in truth_table:
            values, sub_results = row
            for col in columns:
                if col in variables:
                    col_widths[col] = max(col_widths[col], len(str(values.get(col, ""))))
                else:
                    col_widths[col] = max(col_widths[col], len(str(sub_results.get(col, ""))))

        # Print the header row
        header = "  ".join(col.ljust(col_widths[col]) for col in columns)
        print("-" * len(header))
        print(header)
        print("-" * len(header))

        # Print each row of the truth table
        for row in truth_table:
            values, sub_results = row
            row_data = [
                str(values.get(col, "")).ljust(col_widths[col]) if col in variables else str(sub_results.get(col, "")).ljust(col_widths[col])
                for col in columns
            ]
            print("  ".join(row_data))

    except ValueError as e:
        print("Error:", e)


def main():
    args = sys.argv[1:]

    if len(args) == 0:
        print("This is a Propositional Logic Evaluator.")
        print("Enter 'exit' or 'quit' to terminate the program.")

        while True:
            print("\nEnter a propositional logic statement:")
            input_string = input().strip()

            # Exit condition
            if input_string.lower() in {"exit", "quit"}:
                print("Program terminated.")
                break

            evaluate_and_print(input_string)

    elif len(args) == 1:
        filename = args[0]
        try:
            with open(filename, "r") as file:
                statements = file.readlines()

            for statement in statements:
                statement = statement.strip()
                if not statement:
                    continue  # Skip empty lines

                print(f"\nEvaluating: {statement}")
                evaluate_and_print(statement)

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"Error while reading file: {e}")

    else:
        print("Usage:")
        print("  LOGIC                - Run the interactive program")
        print("  LOGIC <filename>     - Evaluate logical statements in the specified file")


if __name__ == "__main__":
    main()
