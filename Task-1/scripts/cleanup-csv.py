def count_lines_with_different_field_counts(file_path, expected_fields=16):
    count = 0
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            # Split the line by the delimiter (comma)
            fields = line.strip().split(',')
            # Check if the number of fields is different from the expected count
            if len(fields) != expected_fields:
                count += 1
                #print(f"Line {line_number}: Found {len(fields)} fields.")
    return count
# Specify your file path
file_path = 'Data/AnalyticalResults.csv'
different_field_count = count_lines_with_different_field_counts(file_path)
print(f"Number of lines with a different number of fields: {different_field_count}")
def split_csv_by_field_count(file_path, expected_fields=16):
    with open(file_path, 'r') as file:
        lines_16 = []
        lines_non_16 = []
        
        for line_number, line in enumerate(file, start=1):
            # Split the line by the delimiter (comma)
            fields = line.strip().split(',')
            
            # Check if the number of fields is 16 or not
            if len(fields) == expected_fields:
                lines_16.append(line)
            else:
                lines_non_16.append(line)
                #print(f"Line {line_number}: Found {len(fields)} fields.")
    # Write the lines with 16 fields to a new file
    with open('Data/AnalyticalResults-cleanup1.csv', 'w') as file_16:
        file_16.writelines(lines_16)
    
    # Write the lines with non-16 fields to another new file
    """with open('Data/AnalyticalResults-census-non16.csv', 'w') as file_non_16:
        file_non_16.writelines(lines_non_16)"""
    print(f"Separated lines into {len(lines_16)} lines with 16 fields and {len(lines_non_16)} lines with non-16 fields.")
# Specify your file path
#file_path = 'Data/AnalyticalResults-census.csv'
split_csv_by_field_count(file_path)