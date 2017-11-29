import csv


def read_mix_set(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            if line['handle'] == "realDonaldTrump":
                data.append(line['text'])
    return data


def read_pure_set(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append(line['Tweet_Text'])
    return data


def read_pure_set_bis(filename):
    data = []
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for line in reader:
            data.append(line['Text'])
    return data


# data_set = read_mix_set('clinton-trump-tweets.csv')
# print(len(data_set))
# data_set = read_pure_set('trump-tweets.csv')
# print(len(data_set))
data_set = read_pure_set_bis('trump-tweets-bis.csv')
print(len(data_set))


for line in data_set[:10]:
    print(line)



