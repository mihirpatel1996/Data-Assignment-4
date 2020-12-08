import csv


def main():
    counter = 0
    writer = csv.writer(open('sudeste.csv/new_file.csv', 'w', newline=''))
    with open('sudeste.csv/sudeste.csv') as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        max_values = False
        for row in csv_reader:

            if(line_count == 500536):
                break

            if(counter <= 100):
                # print(row[0])
                writer.writerow(row)
                counter = counter+1

            if(counter > 100 and temp != row[0]):
                counter = 0
                # print(row[0])
                writer.writerow(row)
                counter = counter+1

            line_count = line_count+1
            print(line_count)
            temp = row[0]

        '''if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1'''


if __name__ == "__main__":
    main()
