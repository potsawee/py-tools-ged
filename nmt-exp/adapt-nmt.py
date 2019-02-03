import sys
import os
import tensorflow as tf
import random
seq2seq_repo = '/home/alta/BLTSpeaking/ged-pm574/local/seq2seq/'
sys.path.insert(0, seq2seq_repo)

from model import EncoderDecoder
from train import construct_training_data_batches
from helper import write_config, read_config

def adapt(config):
    if 'X_SGE_CUDA_DEVICE' in os.environ:
        print('running on the stack...')
        cuda_device = os.environ['X_SGE_CUDA_DEVICE']
        print('X_SGE_CUDA_DEVICE is set to {}'.format(cuda_device))
        os.environ['CUDA_VISIBLE_DEVICES'] = cuda_device

    else: # development only e.g. air202
        print('running locally...')
        os.environ['CUDA_VISIBLE_DEVICES'] = '3' # choose the device (GPU) here

    sess_config = tf.ConfigProto()

    batches, vocab_size, src_word2id, tgt_word2id = construct_training_data_batches(config)

    tgt_id2word = list(tgt_word2id.keys())

    params = {'vocab_src_size': len(src_word2id),
            'vocab_tgt_size': len(tgt_word2id),
            'go_id':  tgt_word2id['<go>'],
            'eos_id':  tgt_word2id['</s>']}


    # build the model
    model = EncoderDecoder(config, params)
    model.build_network()

    # -------- Adaption work -------- #
    bias_name = 'decoder/decode_with_shared_attention/decoder/dense/bias:0'
    weight_name = 'decoder/decode_with_shared_attention/decoder/dense/kernel:0'
    param_names = [bias_name, weight_name]
    # param_names = [var.name for var in tf.trainable_variables()]
    model.adapt_weights(param_names)
    # ------------------------------- #

    new_save_path = config['save']
    if not os.path.exists(new_save_path):
        os.makedirs(new_save_path)
    write_config(new_save_path+'/config.txt', config)

    # save & restore model
    saver = tf.train.Saver(max_to_keep=1)
    save_path = config['load']
    model_number = config['model_number'] if config['model_number'] != None else config['num_epochs'] - 1
    full_save_path_to_model = save_path + '/model-' + str(model_number)

    with tf.Session(config=sess_config) as sess:
        # Restore variables from disk.
        saver.restore(sess, full_save_path_to_model)

        for epoch in range(10):
            print("num_batches = ", len(batches))

            random.shuffle(batches)

            for i, batch in enumerate(batches):
                feed_dict = { model.src_word_ids: batch['src_word_ids'],
                            model.tgt_word_ids: batch['tgt_word_ids'],
                            model.src_sentence_lengths: batch['src_sentence_lengths'],
                            model.tgt_sentence_lengths: batch['tgt_sentence_lengths'],
                            model.dropout: config['dropout']}

                _ = sess.run([model.adapt_op], feed_dict=feed_dict)

                if i % 100 == 0:
                    # to print out training status

                    if config['decoding_method'] != 'beamsearch':
                        [train_loss, infer_loss] = sess.run([model.train_loss, model.infer_loss], feed_dict=feed_dict)
                        print("batch: {} --- train_loss: {:.5f} | inf_loss: {:.5f}".format(i, train_loss, infer_loss))

                    else:
                        # --- beam search --- #
                        [train_loss] = sess.run([model.train_loss], feed_dict=feed_dict)
                        print("BEAMSEARCH - batch: {} --- train_loss: {:.5f}".format(i, train_loss))

                    sys.stdout.flush()

            model.increment_counter()
            print("################## EPOCH {} done ##################".format(epoch))
            saver.save(sess, new_save_path + '/model', global_step=epoch)

def main():
    trained_model = '/home/alta/BLTSpeaking/ged-pm574/nmt-exp/lib/models/correction/scheduled-copy'
    config_path = trained_model + '/config.txt'
    config = read_config(config_path)

    adapt_set = 3
    print('ADAPTION SET: ', str(adapt_set))
    adapt_train_src = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/dtal-m2/split/set{}/train.gec.src'.format(adapt_set)
    adapt_train_tgt = '/home/alta/BLTSpeaking/ged-pm574/gec-lm/lib/dtal-m2/split/set{}/train.gec.tgt'.format(adapt_set)
    adapt_save = 'lib/models/adapt/24jan/set{}-flayer'.format(adapt_set)

    if not os.path.exists(adapt_save):
        os.makedirs(adapt_save)

    # ---------------------------------------- #
    del config['train_src']
    del config['train_tgt']
    del config['save']
    del config['load']

    # ---------- manual seting here ---------- #
    config['train_src'] = adapt_train_src
    config['train_tgt'] = adapt_train_tgt
    config['save'] = adapt_save
    config['load'] = trained_model
    config['model_number'] = 9

    config['learning_rate'] = config['learning_rate']/10

    # ---------------------------------------- #
    # train_src, train_tgt, vocab_src, vocab_tgt
    # batch_size, max_sentence_length

    adapt(config)

if __name__ == '__main__':
    main()
