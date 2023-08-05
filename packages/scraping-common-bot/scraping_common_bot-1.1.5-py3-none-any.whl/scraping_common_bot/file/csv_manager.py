import csv
import shutil
import logger


def append_array_to_csv_file(csv_file_path: str, csv_array: list):
    with open(csv_file_path, 'a') as csv_file:
        writer = csv.writer(csv_file)
        for csv_row in csv_array:
            writer.writerow(csv_row.__dict__.values())
            logger.debug('Inserted in to csv file {} row: {}'
                         .format(csv_file.name, csv_row.__dict__.values()))


def clean_csv_file(csv_blank_file_path: str, csv_file_path: str):
    shutil.copyfile(csv_blank_file_path, csv_file_path)
    logger.debug('Cleaned file: {}'.format(csv_blank_file_path))
