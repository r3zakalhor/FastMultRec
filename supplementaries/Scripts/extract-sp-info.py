import re
import csv
import os,sys


def process_input_file(species_id, input_file, output_csv):
    file = open(input_file, 'r')
    lines = file.readlines()
    flag = False

    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csv_headers = ['gene id', 'gene tree', 'simphy mapping', 'simphy event', 'greedy mapping', 'greedy event']
        csvwriter.writerow(csv_headers)

    genetree = 1

    for line in lines:
        if "</GENETREES>" in line:
            flag = False
            # print(line)
        if flag:
            genetree = genetree + 1
            # reading each word
            for word in re.split('[( )]', line):
                # displaying the words
                # print(word)
                section = re.split('_', word)
                if section.__len__() > 3:
                    if section[1] == species_id:
                        section[4] = section[4].replace(',', '')
                        #print(section)
                        with open(output_csv, 'a', newline='') as csvfile:
                            # Create a CSV writer object
                            csvwriter = csv.writer(csvfile)
                            # Add a new row to the CSV file
                            new_row = [section[0], genetree, section[1], section[2], section[3], section[4]]  # Replace with your actual values
                            csvwriter.writerow(new_row)

        if "<GENETREES>" in line:
            flag = True


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py input_file output_csv species_id")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    species_id = sys.argv[3]

    process_input_file(species_id, input_file, output_csv)