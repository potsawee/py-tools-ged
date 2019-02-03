import sys

def add(input):
    with open(input, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip() + ' .'
        print(line)

def remove(input):
    with open(input, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip().strip('.')
        print(line)

def main():
    if len(sys.argv) != 3:
        print('usage: read_log.py [add/remove] input')
        return
    _type = sys.argv[1]
    input = sys.argv[2]
    if _type == 'add':
        add(input)
    elif _type == 'remove':
        remove(input)

if __name__ == '__main__':
    main()
