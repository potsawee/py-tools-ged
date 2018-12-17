import sys
from gedprocessor import GedProcessor

def main():
    if(len(sys.argv) != 3):
        print("Usage: python3 gec_processing.py original out")
        return

    original = sys.argv[1]
    out = sys.argv[2]

    processor = GedProcessor(columns=['token', 'error_type','label'])

    # AMI/CTS/Fisher work3
    # processor = GedProcessor(columns=['token'])

    processor.read(original)

    processor.remove_hesitation(input=processor.original)
    processor.remove_partial(input=processor.current)
    processor.map_unclear(input=processor.current)


    processor.truelowercase(input=processor.current, start_tag="</s>", end_tag="</s>")
    processor.remove_punctuation(input=processor.current)

    processor.remove_dm()
    processor.remove_re()
    processor.remove_fs()

    processor.write(out + '.ged.tsv')
    processor.write_gec(out + '.gec.txt')

    # processor.write_gec(out, start_tag='<s>', end_tag='</s>', uppercase=True)

if __name__ == '__main__':
    main()
