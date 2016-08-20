import sys
import json
import os
import os.path

ROOTDIR = "raw_data"
OUTPUTDIR = "data_json"

def parse(path):
    disease_index_map = {}
    with open(path, "r") as file:
        base_index = -1

        for idx, line in enumerate(file):
            columns = line.strip().split(",")
            if base_index == -1:
                if "Northland" in columns:
                    base_index = idx + 1
                continue

            if (idx - base_index) % 2 != 0:
                continue # skip 'case' rows

            disease = columns[0]
            for j in xrange(2, len(columns)):
                dhb_index = j - 1
                if not (disease in disease_index_map):
                    disease_index_map[disease] = {}
                submap = disease_index_map[disease]
                submap[dhb_index] = columns[j]
    return json.dumps(disease_index_map,
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
            print "Converting {0}...".format(file)
            input_path = os.path.join(ROOTDIR, file)
            output_path = os.path.join(OUTPUTDIR, name_and_ext[0] + ".json")
            convert(input_path, output_path)
    print "Done."
