import argparse
from pathlib import Path
from q2_proc import read_file, filter_input, tokenize, get_counts, format_output, write_output


argparser = argparse.ArgumentParser()
argparser.add_argument('--train_file', required=True, type=str)
argparser.add_argument('--test_file', required=True, type=str)
argparser.add_argument('--ratio', required=True, type=str)
argparser.add_argument('--dirs', required=True)
args = argparser.parse_args()

dirs = args.dirs.split()


train = open(Path(args.train_file), 'w')
test = open(Path(args.test_file), 'w')

for dirpath in dirs:
    label = Path(dirpath).name
    #print(label)
    #label = label[0]
    all_dir_files = list(Path(dirpath).iterdir())
    train_split = all_dir_files[:int(len(all_dir_files)*float(args.ratio))]
    test_split = all_dir_files[int(len(all_dir_files)*float(args.ratio)):]

    for trainf in train_split:
        train_lines = read_file(trainf)
        sorted_counts = get_counts(train_lines)
        output_lines = format_output(sorted_counts)
        output_lines.insert(0, label)
        output_lines.insert(0, str(trainf))
        output = str(' '.join(output_lines))
        #print(output)
        train.write(output + '\n')

    for testf in test_split:
        test_lines = read_file(testf)
        sorted_counts = get_counts(test_lines)
        output_lines = format_output(sorted_counts)
        output_lines.insert(0, label)
        output_lines.insert(0, str(testf))
        output = str(' '.join(output_lines))
        test.write(output + '\n')

