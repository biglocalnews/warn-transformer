import csv

def write_rows_to_csv(rows, output_path, mode='w'):
    with open(output_path, mode, newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


def write_dict_rows_to_csv(path, headers, rows, mode='w', extrasaction='raise'):
    with open(path, mode, newline='') as out:
        writer = csv.DictWriter(out, fieldnames=headers, extrasaction=extrasaction)
        if mode == 'w':
            writer.writeheader()
        for row in rows:
            writer.writerow(row)
