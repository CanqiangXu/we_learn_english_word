# coding: utf-8
import re


unit_end = [
    "strain",
    "considering",
    "noteworthy",
    "unchallenged",
    "probe",
    "menace",
    "central",
    "prospect",
    "maintain",
    "diversion",
    "require",
    "distort",
    "stabilize",
    "capable",
    "enormous",
    "dose",
    "intensive",
    "superstition",
    "pause",
    "disgrace",
    "abandon",
    "deputy",
    "stripe",
    "commissioner",
    "glimpse",
    "fossil",
    "quantity",
    "blunt",
    "nonsense",
    "incentive"
]


def read_file(filename):
    with open(filename) as f:
        for line in f:
            # print(line)
            yield re.findall(r'.*current_page\': ([0-9]{1,5}).*words\': \'([\s\S]{1,20})\',.*', line)[0]


def write_info_file(filename, line):
    with open(filename, "a+") as f:
        f.write(line + "\n")


def parse():
    words = []
    for line in read_file("data"):
        words.append(line)
    words.sort(key=lambda i: int(i[0]))
    i = 1
    # write_info_file("2020考研英语恋练有词单词.txt", "unit" + str(i))
    for word in words:
        print(word)
        write_info_file("units/unit" + str(i) + ".txt", word[1])
        # write_info_file("2020考研英语恋练有词单词.txt", word[1])
        if word[1] == unit_end[i-1]:
            i += 1

            # write_info_file("2020考研英语恋练有词单词.txt", "unit" + str(i))


if __name__ == '__main__':
    parse()



