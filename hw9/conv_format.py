import sys

def convert(line):
    conv_str = ""
    line = line.strip()
    if line:
        entries = line.split("=>")
        observation = entries[0].strip().split()
        tags = []
        for elem in entries[1].strip().split()[1:-1]:
            tags.append(elem.split("_")[1])
        conv_list = []
        for i in zip(observation, tags):
            conv_list.append(i[0] + "/" + i[1])
        conv_str = " ".join(conv_list)
    print(conv_str)


if __name__ == "__main__":
    for line in sys.stdin:
        convert(line)

