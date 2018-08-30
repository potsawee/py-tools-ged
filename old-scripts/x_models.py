from gedoutparser import GedOutParser

g = GedOutParser(['token', 'label', 'c_prob', 'i_prob'])
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/noattention-fcepub.ged.spell.v2.tsv')
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead1-fcepub.ged.spell.v2.tsv')
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead2-fcepub.ged.spell.v2.tsv')
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead5-fcepub.ged.spell.v2.tsv')
# g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multihead10-fcepub.ged.spell.v2.tsv')
# g.x_models(0,1, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/no_vs_multi1.png')
# g.x_models(0,2, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/no_vs_multi2.png')
# g.x_models(0,3, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/no_vs_multi5.png')
# g.x_models(0,4, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/no_vs_multi10.png')
# g.x_models(1,2, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead/multi1_vs_multi2.png')

# Multihead Experiment v2
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/noattention-fcepub.ged.spell.v2.tsv')
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead1-fcepub.ged.spell.v2.tsv')
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead2-fcepub.ged.spell.v2.tsv')
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead5-fcepub.ged.spell.v2.tsv')
g.read('/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multihead10-fcepub.ged.spell.v2.tsv')
g.x_models(0,1, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/no_vs_multi1.png')
g.x_models(0,2, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/no_vs_multi2.png')
g.x_models(0,3, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/no_vs_multi5.png')
g.x_models(0,4, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/no_vs_multi10.png')
g.x_models(1,2, '/home/alta/BLTSpeaking/ged-pm574/attention-word/posterior/multihead-v2/multi1_vs_multi2.png')



# g = GedOutParser()
# g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2/output/1-Marek.tsv', skip_options=[1])
# g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2/output/2-TLC.tsv', skip_options=[1])
# g.x_models(0,1, '/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2/output/x_models.png')
