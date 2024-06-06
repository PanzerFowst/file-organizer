#!/bin/bash

concatenate_files() {

  # Define the output file:
  local output_file="./output_file.txt"

  # Define the directory to search for input files:
  local include_directory="./app/"

  # Define the pattern for the files to include (e.g., "*.py" for Python files):
  local file_pattern="*.py"


  # Create an array called "input_files" based on the include directory and pattern:
  local input_files=($(find "$include_directory" -name "$file_pattern"))

  # Verify the input files array is not empty:
  if [ ${#input_files[@]} -eq 0 ]; then
    echo "No input files specified."
    return 1
  fi

  # Print the input_files array:
  echo "Input files found:"
  for file in "${input_files[@]}"; do
    echo "$file"
  done

  # Wait until any key is pressed to continute concatinating files:
  echo
  echo "Ready to concatinate all files together into the output file ($output_file)."
  echo "Note that this will CLEAR the output file ($output_file) of all its contents before writing to it!"
  echo
  echo "Press any key to continue..."
  read -n 1 -s -r -p "" || true
  echo

  # Empty the output file if it exists:
  > "$output_file"

  # Concatenate all input files into the output file with newlines between each:
  for file in "${input_files[@]}"; do
    cat "$file" >> "$output_file"
    echo "" >> "$output_file"
  done

  # Verify if the concatenation was successful:
  if [ $? -eq 0 ]; then
    echo "Files concatenated successfully into $output_file"
  else
    echo "An error occurred while concatenating files"
    return 1
  fi

  return 0
}


# Call the function:
concatenate_files

# Countdown timer for exiting the script:
countdown_time=5
while [ $countdown_time -ge 0 ]; do
  if [ $countdown_time -eq 1 ]; then
    seconds_str="second"
  else
    seconds_str="seconds"
  fi
  echo -ne "Exiting in $countdown_time $seconds_str or press any key to exit immediately...\r"
  read -t 1 -n 1 key
  if [ $? -eq 0 ]; then
    # Key was pressed
    break
  fi
  ((countdown_time--))
done

# Place additional whitespace between script and next line for the end:
echo
echo
