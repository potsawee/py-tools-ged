"""
/home/dawna/material/Tools_V1.3/lbin/rnnlm
-ppl
-readmodel train-rnnlm/rnnlms/v3/one-billion/RNN_weight.OOS.cuedrnnlm.rnnlm.300.300/train_LM.wgt.iter9
-testfile tmp/test_ppl.txt
-inputwlist train-rnnlm/rnnlms/v3/one-billion/lib/wlists/train.lst.index
-outputwlist train-rnnlm/rnnlms/v3/one-billion/lib/wlists/train.lst.index
-fullvocsize 64002
-debug 2
"""

import subprocess
import pdb
import math
import sys

class PplParser(object):
    def __init__(self):
        self.cmd = []
        self.outputs = []

    # def make_cmd(self, model, testfile, inputwlist, outputwlist, vocabsize, intermediatefile, debug="2"):
    #     rnnlmbin = "/home/dawna/material/Tools_V1.3/lbin/rnnlm"
    #     self.cmd = [rnnlmbin, "-ppl"]
    #     self.cmd += ["-readmodel", model]
    #     self.cmd += ["-testfile", testfile]
    #     self.cmd += ["-inputwlist", inputwlist]
    #     self.cmd += ["-outputwlist", outputwlist]
    #     self.cmd += ["-fullvocsize", vocabsize]
    #     self.cmd += ["-debug", debug]
    #     self.cmd += [">", intermediatefile]

    def run(self):
        print("start cmd")
        # p = subprocess.Popen(self.cmd, stdout=subprocess.PIPE)
        # self.outputs = p.communicate()
        # p.wait()
        _ = subprocess.call(self.cmd)
        print("finish cmd")
        return p.returncode

    def parse_output(self, pplpath):
        eos = "</s>"
        with open(pplpath) as file:
            lines = file.readlines()

        sent_log_prob = 0
        word_count = 0
        sent_log_probs = []
        for line in lines[26:-4]:
            id, prob, word = line.split()
            prob = float(prob)
            if word == eos: # end of sentence
                sent_log_prob += math.log(prob)
                word_count += 1
                sent_log_probs.append(sent_log_prob / word_count)

                sent_log_prob = 0
                word_count = 0
            else:
                sent_log_prob += math.log(prob)
                word_count += 1

        # with open(outpath, 'w') as file:
        #     for i, logprob in enumerate(sent_log_probs):
        #         file.write("rank {:2d}th:  {:.5f}\n".format(i+1, logprob))
        for logprob in sent_log_probs:
            print(logprob)

        # for line in lines:
        #     if
        # probabilities = []

def main():
    if len(sys.argv) != 2:
        print("usage: python3 ppl_parser.py input")
        return

    path = sys.argv[1]

    p = PplParser()
    p.parse_output(path)

if __name__ == '__main__':
    main()
