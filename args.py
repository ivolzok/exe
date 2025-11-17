import argparse


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='путь до файла')
    args = parser.parse_args()
    return args
