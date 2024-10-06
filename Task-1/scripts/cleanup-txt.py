# Set the file paths
input_file_path = "Data/AgChange/AgCensus_MasterDataFrame-cropped.txt"
output_cleaned_file_path = "Data/AgChange/AgCensus_MasterDataFrame-cleaned.txt"
output_filtered_file_path = "Data/AgChange/AgCensus_MasterDataFrame-cleaned.txt"

# Initialize counters
removed_lines_count = 0
cleaned_lines = []
filtered_lines = []
total_lines = 0

# Read the input file and process each line
with open(input_file_path, 'r') as infile:
    for line in infile:
        # Strip whitespace and split by tab
        elements = line.strip().split('\t')
        # Check if the line has exactly 84 elements
        if len(elements) == 84:
            cleaned_lines.append(line.strip())
        else:
            filtered_lines.append(line.strip())  # Store the removed lines
            removed_lines_count += 1
        total_lines += 1

# Write the cleaned lines to the output cleaned file
with open(output_cleaned_file_path, 'w') as outfile:
    for cleaned_line in cleaned_lines:
        outfile.write(cleaned_line + '\n')

# Write the removed lines to the output filtered file
with open(output_filtered_file_path, 'w') as outfile:
    for filtered_line in filtered_lines:
        outfile.write(filtered_line + '\n')

# Output the number of removed lines and original lines
print(f"Number of lines cut out: {removed_lines_count}")
print(f"Number of original lines: {total_lines}")
