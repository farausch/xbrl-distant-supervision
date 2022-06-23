from shutil import copyfile
from os import listdir, path
from os.path import isfile

class IOHelper:

    def get_all_financial_statement_files(self, directory, extension):
        return [path.join(directory, f) for f in listdir(directory) if isfile(path.join(directory, f)) and f.endswith(extension)]
    
    def get_ground_truth_triplets(self, ground_truth_file):
        ground_truth_file = open(ground_truth_file, "r")
        current_line = 0
        lines = []
        xbrl_files = []
        tokens = []
        annotations = []
        for line in ground_truth_file:
            lines.append(line)
        ground_truth_file.close()
        while current_line < len(lines):
            xbrl_files.append(lines[current_line].replace("\n", ""))
            tokens.append(lines[current_line + 1].replace("\n", ""))
            annotations.append(lines[current_line + 2].replace("\n", "").lower())
            current_line += 3
        return xbrl_files, tokens, annotations