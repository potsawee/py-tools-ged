import sys
seq2seq_repo = '/home/alta/BLTSpeaking/ged-pm574/local/seq2seq/'
sys.path.insert(0, seq2seq_repo)

import os
import numpy as np
import tensorflow as tf
import argparse
import subprocess
import pdb

from model import EncoderDecoder
from helper import load_vocab, read_config

'''
Translating source sentences to target sentences using a trained model
'''

def get_translate_arguments(parser):
    '''Arguments for translating'''
    # file paths
    parser.add_argument('--load', type=str, required=True)  # path to load model
    parser.add_argument('--srcfile', type=str, required=True)
    parser.add_argument('--tgtfile', type=str, required=True)
    parser.add_argument('--model_number', type=int, default=None)

    return parser

def src_data(srcfile, src_word2id, max_sentence_length):
    src_sentences = []
    with open(srcfile, 'r') as file:
        for line in file:
            src_sentences.append(line.strip())

    src_sent_ids = []
    for sentence in src_sentences:
        ids = []
        for word in sentence.split():
            if word in src_word2id:
                ids.append(src_word2id[word])
            else:
                ids.append(src_word2id['<unk>'])
        src_sent_ids.append(ids)

    # check if each sentence is too long
    for i in range(len(src_sent_ids)):
        if len(src_sent_ids[i]) > max_sentence_length:
            src_sent_ids[i] = src_sent_ids[i][:max_sentence_length]

    src_sent_len = [len(sent) for sent in src_sent_ids]
    src_sent_ids = [ids + [src_word2id['</s>']]*(max_sentence_length-len(ids)) for ids in src_sent_ids]

    return src_sent_ids, src_sent_len

def translate(config):
    if 'X_SGE_CUDA_DEVICE' in os.environ:
        print('running on the stack...')
        cuda_device = os.environ['X_SGE_CUDA_DEVICE']
        print('X_SGE_CUDA_DEVICE is set to {}'.format(cuda_device))
        os.environ['CUDA_VISIBLE_DEVICES'] = cuda_device

    else: # development only e.g. air202
        print('running locally...')
        os.environ['CUDA_VISIBLE_DEVICES'] = '0' # choose the device (GPU) here

    sess_config = tf.ConfigProto()

    vocab_paths = {'vocab_src': config['vocab_src'], 'vocab_tgt': config['vocab_tgt']}
    src_word2id, tgt_word2id = load_vocab(vocab_paths)

    tgt_id2word = list(tgt_word2id.keys())

    params = {'vocab_src_size': len(src_word2id),
            'vocab_tgt_size': len(tgt_word2id),
            'go_id':  tgt_word2id['<go>'],
            'eos_id':  tgt_word2id['</s>']}

    # build the model
    model = EncoderDecoder(config, params)
    model.build_network()

    # save & restore model
    saver = tf.train.Saver()
    save_path = config['load']
    model_number = config['model_number'] if config['model_number'] != None else config['num_epochs'] - 1
    full_save_path_to_model = save_path + '/model-' + str(model_number)


    # ------ PPL Parser for Fluency Score ------ #
    # parser = PplParser()
    # rnnlm_model = "/home/alta/BLTSpeaking/ged-pm574/gec-lm/train-rnnlm/rnnlms/v3/one-billion/RNN_weight.OOS.cuedrnnlm.rnnlm.300.300/train_LM.wgt.iter9"
    # # test_file = "/home/alta/BLTSpeaking/ged-pm574/nmt-exp/tmp/translate_ppl.txt"
    # test_file = config['tgtfile']
    # intermediatefile = "tmp/trans-intermediate.txt"
    # inputwlist = "/home/alta/BLTSpeaking/ged-pm574/gec-lm/train-rnnlm/rnnlms/v3/one-billion/lib/wlists/train.lst.index"
    # outputwlist = "/home/alta/BLTSpeaking/ged-pm574/gec-lm/train-rnnlm/rnnlms/v3/one-billion/lib/wlists/train.lst.index"
    # vocabsize = "64002"
    # parser.make_cmd(rnnlm_model, test_file, inputwlist, outputwlist, vocabsize, intermediatefile)
    # ------------------------------------------ #

    with tf.Session(config=sess_config) as sess:
        # Restore variables from disk.
        saver.restore(sess, full_save_path_to_model)
        # print("Model restored")

        src_sent_ids, src_sent_len = src_data(config['srcfile'], src_word2id, config['max_sentence_length'])

        num_sentences = len(src_sent_ids)
        batch_size = 1000
        num_batches = int(num_sentences/batch_size) + 1

        print('num_batches =', num_batches)

        beam_width = config['beam_width']

        outputs = []

        for i in range(num_batches):

            i_start = batch_size*i
            i_end = i_start+batch_size if i_start+batch_size <= num_sentences else num_sentences
            translate_dict = {model.src_word_ids: src_sent_ids[i_start:i_end],
                        model.src_sentence_lengths: src_sent_len[i_start:i_end],
                        model.dropout: 0.0}

            predicted_ids = sess.run(model.predicted_ids, feed_dict=translate_dict)

            for sentence in predicted_ids:
                beam = []
                for k in range(beam_width):
                    translation = sentence[:,k]
                    words = []
                    for id in translation:
                        if id == params['eos_id']:
                            break

                        words.append(tgt_id2word[id])

                    beam.append(words)

                outputs.append(beam)

            print('#', end='')
            sys.stdout.flush()

        print("num outputs: ", len(outputs))
        # for i in range(len(outputs)):
        #     if len(outputs[i]) != 10:
        #         pdb.set_trace()
        # print("no problem!")
        # pdb.set_trace()

        with open(config['tgtfile'], 'w', encoding="utf8") as file:
            for output in outputs:
                for beam in output:
                    x = "<s> " + " ".join(beam[:-1]).upper() + " </s>\n"
                    file.write(x)




def main():
    # get configurations from the terminal
    parser = argparse.ArgumentParser()
    parser = get_translate_arguments(parser)
    args = vars(parser.parse_args())

    config_path = args['load'] + '/config.txt'
    config = read_config(config_path)
    config['load'] = args['load']
    config['srcfile'] = args['srcfile']
    config['tgtfile'] = args['tgtfile']
    config['model_number'] = args['model_number']

    translate(config=config)

if __name__ == '__main__':
    main()
