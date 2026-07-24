# Lab 1: Grade Evaluator and Archiver

This project has two main parts: a Python program and a Bash script.

## Project Files

```text
lab1/
├── grade-evaluator.py
├── organizer.sh
├── grades.csv
└── README.md
```

## Grade Evaluator

The `grade-evaluator.py` program reads student marks from `grades.csv`.

It checks that:

* Every score is between 0 and 100.
* Formative assignment weights add up to 60%.
* Summative assignment weights add up to 40%.
* All assignment weights add up to 100%.

The program calculates the student's final grade and GPA using:

```text
GPA = (Final Grade / 100) × 5
```

A student passes only when they score at least 50% in both the Formative and Summative categories.

When a student fails a Formative assignment, the program identifies the failed assignment with the highest weight for resubmission. When several assignments have the same highest weight, all of them are shown.

Run the Python program using:

```bash
python3 grade-evaluator.py
```

## Grade Archiver

The `organizer.sh` script manages the `grades.csv` file after the grades have been evaluated.

It:

* Creates an `archive` folder when one does not exist.
* Adds the current date and time to the name of `grades.csv`.
* Moves the renamed file into the `archive` folder.
* Creates a new empty `grades.csv` file.
* Records the archiving details in `organizer.log`.

Run the script using:

```bash
chmod +x organizer.sh
./organizer.sh
```

## Recommended Steps

1. Add the student's grades to `grades.csv`.
2. Run `grade-evaluator.py` to calculate the result.
3. Run `organizer.sh` to archive the old grades file.
4. Use the new empty `grades.csv` for the next student or set of grades.

## Learning Objectives

This lab teaches how to:

* Read and process CSV files using Python.
* Use conditions to validate data and determine pass or fail results.
* Calculate weighted grades and GPA.
* Use Bash scripts to organise files.
* Create timestamps and maintain log files.

## Required Submission Files

The GitHub repository must contain:

```text
grade-evaluator.py
organizer.sh
README.md
```
