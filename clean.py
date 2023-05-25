import os
import re

def read_file_into_set(filename):
    with open(filename, 'r') as f:
        return {line.strip() for line in f}

def write_set_into_file(filename, data):
    invalid_numbers = 0
    with open(filename, 'w') as f:
        for item in data:
            valid, number = validate_UK_mobile_number(item)
            if valid:
                f.write("%s\n" % number)
            else:
                invalid_numbers += 1
    return invalid_numbers

def validate_UK_mobile_number(number):
    # Remove all spaces
    number = number.replace(" ", "")

    # UK mobile numbers start with '07' or '+447' followed by 9 more digits.
    # The regex pattern below validates this.
    pattern = re.compile("^(07|\+447)\d{9}$")

    return bool(pattern.match(number)), number

def main():
    # Read data from files into sets (automatically removes duplicates)
    mobile_data = read_file_into_set('mobile_numbers_TPS_FINAL.txt')
    blacklist = read_file_into_set('blacklist.txt')

    # Subtract the blacklist set from the mobile data set
    cleaned_data = mobile_data - blacklist

    # Create directory if it doesn't exist
    os.makedirs('safe', exist_ok=True)

    # Write the cleaned and validated data to the output file
    invalid_numbers = write_set_into_file(os.path.join('safe', 'mobile_data_cleaned.txt'), cleaned_data)

    # Print summary
    print("Summary:")
    print(f"Read {len(mobile_data)} lines from mobile_data.txt")
    print(f"Read {len(blacklist)} lines from blacklist.txt")
    print(f"Removed {len(mobile_data) - len(cleaned_data)} lines based on blacklist")
    print("Removed duplicates")
    print(f"Wrote {len([line for line in cleaned_data if validate_UK_mobile_number(line)[0]])} lines to safe/mobile_data_cleaned.txt")
    print(f"Found {invalid_numbers} invalid numbers")

if __name__ == '__main__':
    main()
