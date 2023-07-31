# `gradesculptor`

`gradesculptor` simplifies converting submissions of Gradescope's ["Online Assignments"](https://help.gradescope.com/article/gm5cmcz19k-instructor-assignment-online) to plain text files, for use with your own grader, plagiarism checker, etc.

Once you've exported submissions to any given online assignment, you'll receive a CSV—often called `submission_metadata.csv`—from Gradescope. You can use `gradesculptor` to convert that CSV file into a set of plain text files, one for each student's submission.

## Usage

If using Gradescope's defaults as of July 31st, 2023:

```bash
python gradesculptor.py
```

With custom arguments:

```bash
python gradesculptor.py --filename submissions.csv --id-column 'Submission ID' --o 'test_submissions/'
```

`--filename` specifies the CSV file from which to read student submissions. `--id-column` is the name of the column which contains submission IDs. `--o` or `--output` is the directory in which to write the plain text files.

## Requirements

* [`pandas`](https://pandas.pydata.org/)

Can be installed in your environment with `pip install -r requirements.txt`.
