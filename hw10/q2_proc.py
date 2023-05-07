from argparse import ArgumentParser
import re
import collections

def read_file(filename):
    with open(filename, "r") as f:
        lines = [x.strip() for x in f.readlines() if x.strip()]
    return lines

def filter_input(text):
    ftext = re.sub(r'[^a-zA-Z]',' ', text)
    ftext = ftext.lower()
    return ftext

def tokenize(text):
    tokens = [word for word in text.split()]
    return tokens

def get_counts(lines):
    text = ' '.join(lines)
    ftext = filter_input(text)
    tokens = tokenize(ftext)
    counts = {word:0 for word in set(tokens)}
    for word in tokens:
        counts[word] += 1
    #od_counts = collections.OrderedDict(sorted(counts.items()))
    od_counts = dict(sorted(counts.items()))
    return od_counts

def format_output(od_list):
    lines = []
    for token in od_list.keys():
        #print(token)
        lines.append(token+ ' '+str(od_list[token]))
    #print(lines)
    return lines

def write_output(file, lines):
    with open(file, "w") as f:
        for line in lines:
            line = str(line)
            f.write(line+' ')

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--input", type=str, required=True)
    arg_parser.add_argument("--label", type=str, required=True)
    arg_parser.add_argument("--output", type=str, required=True)
    args = arg_parser.parse_args()

    input_file = read_file(args.input)
    label = args.label
    output_file = args.output

    sorted_counts = get_counts(input_file)
    #print(sorted_counts)
    output_lines = format_output(sorted_counts)
    output_lines.insert(0, str(args.label))
    output_lines.insert(0, str(args.input))
    write_output(output_file, output_lines)
