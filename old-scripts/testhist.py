from gedoutparser import GedOutParser

# g = GedOutParser()
g = GedOutParser(['token', 'label', 'c_prob', 'i_prob'])
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/noattention-fcepub.ged.spell.v2.tsv', name="NoAttention")
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead1-fcepub.ged.spell.v2.tsv', name="Multihead 1")
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead2-fcepub.ged.spell.v2.tsv', name="Multihead 2")
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead5-fcepub.ged.spell.v2.tsv', name="Multihead 5")
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead10-fcepub.ged.spell.v2.tsv', name="Multihead 10")
#
# g.histogram(indices=[0,1], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/hist-1.png')
# g.histogram(indices=[0,2], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/hist-2.png')
# g.histogram(indices=[0,3], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/hist-5.png')
# g.histogram(indices=[0,4], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/hist-10.png')

# Multihead Experiment v2
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/noattention-fcepub.ged.spell.v2.tsv', name="NoAttention")
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead1-fcepub.ged.spell.v2.tsv', name="Multihead 1")
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead2-fcepub.ged.spell.v2.tsv', name="Multihead 2")
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead5-fcepub.ged.spell.v2.tsv', name="Multihead 5")
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead10-fcepub.ged.spell.v2.tsv', name="Multihead 10")

g.histogram(indices=[0,1], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/hist-1.png')
g.histogram(indices=[0,2], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/hist-2.png')
g.histogram(indices=[0,3], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/hist-5.png')
g.histogram(indices=[0,4], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/hist-10.png')
