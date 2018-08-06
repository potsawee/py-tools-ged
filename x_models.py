from gedoutparser import GedOutParser

g = GedOutParser(['token', 'label', 'c_prob', 'i_prob'])
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/noattention-fcepub.ged.spell.v2.tsv')
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead2-fcepub.ged.spell.v2.tsv')

g.x_models(0,1, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/x_models.png')
