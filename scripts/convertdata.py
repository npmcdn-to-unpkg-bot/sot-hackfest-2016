import sys
import json
import os
import os.path

ROOTDIR = "raw_data"
OUTPUTDIR = "public/data_json"

def parse(path):
    disease_index_list = []
    with open(path, "r") as file:
        alternation_index = -1

        for idx, line in enumerate(file):
            columns = line.strip().split(",")
            if alternation_index == -1:
                if "Northland" in columns:
                    alternation_index = 0
                continue

            count_of_empty = 0
            for col in columns:
                if col.strip() == "":
                    count_of_empty += 1
            if (float(count_of_empty) / len(columns)) > 0.75:
                continue

            alternation_index += 1
            if alternation_index % 2 == 0:
                continue # skip 'case' rows

            disease = columns[0]
            max_cases = 0
            disease_index_list.append({ "name" : disease, "values": [], "max" : 0})
            for j in range(2, len(columns)):
                try:
                    num_cases = int(columns[j])
                except ValueError:
                    continue
                if num_cases > max_cases:
                    max_cases = num_cases
                array = disease_index_list[-1]["values"]
                array.append(num_cases)
            disease_index_list[-1]["max"] = max_cases
    return json.dumps(disease_index_list,
                      sort_keys=True,
                      indent=4, separators=(',', ': '))

def convert(path, output_path):
    with open(output_path, "w") as output_file:
        code = parse(path)
        output_file.write(code)

if __name__ == "__main__":
    try:
        os.mkdir(OUTPUTDIR)
    except OSError:
        pass # Directory already exists
    for subdir, dirs, files in os.walk(ROOTDIR):
        for file in files:
            name_and_ext = os.path.splitext(file)
            if name_and_ext[1] != ".csv":
                continue
            print("Converting {0}...".format(file))
            input_path = os.path.join(ROOTDIR, file)
            output_path = os.path.join(OUTPUTDIR, name_and_ext[0] + ".json")
            convert(input_path, output_path)
    print("Done.")
