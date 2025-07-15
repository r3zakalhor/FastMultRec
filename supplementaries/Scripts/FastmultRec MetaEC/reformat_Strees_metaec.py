from ete3 import Tree
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]



# Open the input file and read its contents
with open(input_file, 'r') as file:
    content = file.read()

# Replace all occurrences of the single quote
content = content.replace("'", "")
content = content.replace(";", "")
# Write the modified content back to the file
with open(output_file, 'w') as file:
    file.write(content)
