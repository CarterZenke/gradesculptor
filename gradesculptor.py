import argparse
import os
import sys
import logging

import pandas as pd


def configure_logging() -> None:
    """
    Configures logging settings.

    Sets the logging level to INFO, configures the message format, and sets the handler to output to stdout.
    """

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def clean_answers(
    filename: str = "submission_metadata.csv",
    submission_id_column: str = "Submission ID",
    output_dir="submissions",
) -> None:
    """
    Reads student submission data from a CSV file and writes each submission's answers to a separate text file.

    Parameters:
    filename (str): The name of the CSV file from which to read student submissions.
    submission_id_column (str): The name of the column in the CSV file that contains the submission IDs. Defaults to "Submission ID".
    output_dir (str): The path to the directory where the output files will be written. Defaults to "submissions".
    """

    # Read CSV
    df = pd.read_csv(filename, dtype={submission_id_column: str}, na_values=None)

    # Filter rows to submitted
    df = df[df[submission_id_column].notna()]
    logging.info(f"Number of submissions to parse: {len(df)}")

    # Filter columns to those with answer content and submission ID
    df = df.filter(
        regex=rf"(?:^Question \d\d?(?:\.\d\d?)? Response$)|(?:{submission_id_column})",
        axis=1,
    )

    # Define length of question header for .txt file
    header_length = longest_column_length(df.columns) + 20

    # Write submissions to .txt files
    for _, student_submission in df.iterrows():

        # Create directory for file
        submission_id = student_submission[submission_id_column]
        os.makedirs(f"{output_dir}/{submission_id}", exist_ok=True)

        # Write submission
        with open(f"{output_dir}/{submission_id}/written_answers.txt", "w") as f:

            def write_to_txt(column_name, value) -> None:
                f.write(build_header(column_name, header_length))

                f.write(str(value) + "\n")

                f.write(("-" * header_length) + "\n\n")

            for column_name, value in student_submission.items():
                write_to_txt(column_name, value)


def build_header(column_name: str, header_length: int) -> str:
    """
    Constructs a header string of a given length, with the column name centered and surrounded by dashes.

    Parameters:
    column_name (str): The name of the column to center in the header.
    header_length (int): The total length of the header string.

    Returns:
    str: The constructed header string.
    """

    # Calculate number of dashes
    num_dashes = header_length - len(column_name)
    first_dash_length = num_dashes // 2

    # Odd or even number of dashes
    if num_dashes % 2 == 0:
        second_dash_length = first_dash_length
    else:
        second_dash_length = first_dash_length + 1

    # Define header
    header = ("-" * first_dash_length) + column_name + ("-" * second_dash_length) + "\n"
    return header


def longest_column_length(columns: list[str]) -> int:
    """
    Determines the length of the longest column name in a list of column names.

    Parameters:
    columns (list[str]): A list of column names.

    Returns:
    int: The length of the longest column name.
    """
    max_column_name_length = 0
    for column_name in columns:
        if len(column_name) > max_column_name_length:
            max_column_name_length = len(column_name)

    return max_column_name_length


def csv_filename(filename: str) -> bool:
    if not filename.endswith(".csv"):
        return False
    return True


def main():

    configure_logging()

    # Configure command-line arguments
    parser = argparse.ArgumentParser(description="Parse and clean student submissions.")
    parser.add_argument(
        "--filename",
        type=argparse.FileType("r"),
        default="submission_metadata.csv",
        help="The filename of the CSV file to read data from.",
    )
    parser.add_argument(
        "--id-column",
        type=str,
        default="Submission ID",
        help="The name of the column in the CSV file that contains the submission IDs.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="submissions",
        help="The path to the directory where the output files will be written.",
    )

    # Parse arguments
    args = parser.parse_args()
    if not csv_filename(str(args.filename.name)):
        logging.info(f"Must read from a CSV file.")
        return

    logging.info(f"Cleaning answers.")
    clean_answers(args.filename.name, args.id_column, args.output)

    logging.info(f"Done.")


if __name__ == "__main__":
    main()
