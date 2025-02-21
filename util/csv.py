import csv


def csv_export(
    data: list,
    filename: str,
    delimiter: str = ",",
    quotechar: str = '"',
    quoting=csv.QUOTE_MINIMAL,
):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(
            csvfile, delimiter=delimiter, quotechar=quotechar, quoting=quoting
        )
        for row in data:
            writer.writerow(row)
