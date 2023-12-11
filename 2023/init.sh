#!/bin/sh

day=$1

if [ -z "$day" ]; then
  # If the day is not specified, try to get it from the directory
  last_file=$(ls day*.py | tail -n 1)
  # Extract the number from this file
  day=${last_file%%.py}
  day=${day##day}
  # Increment it by 1
  day=$(echo "$day+1" | bc)
fi

filename=$(printf 'day%02d' $day)
input_filename="input_$filename.txt"
filename="$filename.py"
if [ -f "$filename" ]; then
  echo "$filename already exists. Exiting."
  exit 1
fi

# Get the title from the advent of code website
wget --quiet "https://adventofcode.com/2023/day/$day" -O tempAOCpage
title=$(grep -- '--- Day' tempAOCpage |\
  sed -E 's/.*--- Day(.*)---.*/\1/' |\
  cut -d: -f2 |\
  xargs)  # Remove leading and trailing spaces

echo "Initializing Day $day: $title"

# Copy the template and fill in the header
sed 's/Day <++>/Day '$(printf '%02d' $day)": $title/" template.py > $filename

# Download the data file
if [ -f "cookies.txt" ]; then
  wget --quiet --load-cookies=cookies.txt "https://adventofcode.com/2023/day/$day/input" -O $input_filename
else
  echo "Can't download the input without session cookies for adventofcode.com."
fi

# Extract the example from the webpage and remove all tags
sed -n '/<pre>/,/<\/pre>/p' tempAOCpage |\
  sed -E 's/(<pre>|<code>|<\/code>|<\/pre>)//g' > "test.txt"

# Remove the tempAOCpage
rm tempAOCpage

# Open the input files for double checking and then the code file
vim -p "test.txt" $input_filename $filename
