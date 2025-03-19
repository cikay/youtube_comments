import csv

# Read the CSV file and sort it
with open("train.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=";")
    header = next(reader)  # Read the header
    sorted_rows = sorted(reader, key=lambda row: row[0])  # Sort by wrong_sentence

# Write the sorted data back to a new file
with open("sorted_file.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(header)  # Write the header
    writer.writerows(sorted_rows)  # Write sorted rows

print("Sorting complete! Check 'sorted_file.csv'.")
