class Convertor(object):
    def __init__(self):
        pass

    def read_map(self, path):
        with open(path, 'r') as f:
            lines = f.readlines()
            # line e.g. S4Z9HEYRGU CBL311-01266
            # Cambridge English <=> CUED
        self.ce_to_cued = {}
        self.cued_to_ce = {}
        for line in lines:
            ce, cued = line.split()
            self.ce_to_cued[ce] = cued
            self.cued_to_ce[cued] = ce

    def read_grade(self, path, skip_firstline=True):
        with open(path, 'r') as f:
            lines = f.readlines()
        if skip_firstline:
            lines = lines[1:]
        self.cued_to_grade = {}
        for line in lines:
            id, score = line.split()
            score = float(score) / 5 # scale down from 30
            if(score < 2.0 and score > 0.0):
                grade = 'A1'
            elif(score < 3.0):
                grade = 'A2'
            elif(score < 4.0):
                grade = 'B1'
            elif(score < 5.0):
                grade = 'B2'
            elif(score < 6.0):
                grade = 'C'
            else:
                grade = '?'

            self.cued_to_grade[id] = grade

def main():
    mapping_file = '/home/alta/BLTSpeaking/convert-v2/4/lib/spId/BLXXXeval3-map.lst'
    grading_file = '/home/alta/BLTSpeaking/grd-graphemic-kmk/GKJ1-HD3/kaldi-mar2017/grader/BLXXXeval3/tg_16.0_0.0_mbr/F3/speaker/data/expert-grades.txt'
    convertor = Convertor()
    convertor.read_map(mapping_file)
    convertor.read_grade(grading_file)

    while(True):
        ce_id = input("CE ID: ")
        cued_id = convertor.ce_to_cued[ce_id]
        grade = convertor.cued_to_grade[cued_id]

        print("{}\t{}\t{}".format(ce_id, cued_id, grade))

if __name__ == '__main__':
    main()
