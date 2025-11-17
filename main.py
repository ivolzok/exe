from args import get_args
from pe_file import PEFile
def main():
    #args = get_args()
    #path = args.path
    with open("D:\mongodb-compass.exe", 'rb') as file:
        pe_file = PEFile.from_file(file)
        print('cbbbb')

if __name__ == "__main__":
    main()