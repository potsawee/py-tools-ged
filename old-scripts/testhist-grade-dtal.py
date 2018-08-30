from gedoutparser import GedOutParser

g = GedOutParser()

g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/Compare-Final-Outputs/1-AllGrade-file4.tsv', name='All')
g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/A1/output/4-REMOVE-DM-RE.tsv', name='A1')
g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/A2/output/4-REMOVE-DM-RE.tsv', name='A2')
g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/B1/output/4-REMOVE-DM-RE.tsv', name='B1')
g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/B2/output/4-REMOVE-DM-RE.tsv', name='B2')
g.read('/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/C/output/4-REMOVE-DM-RE.tsv', name='C')


# g.histogram(indices=[0,1,2,3,4,5], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/histograms/hist-1.png')
g.histogram(indices=[0,1], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/histograms/hist-A1.png')
g.histogram(indices=[0,2], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/histograms/hist-A2.png')
g.histogram(indices=[0,3], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/histograms/hist-B1.png')
g.histogram(indices=[0,4], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/histograms/hist-B2.png')
g.histogram(indices=[0,5], bin_num=100, savepath='/home/alta/BLTSpeaking/ged-pm574/clctraining-cued/dtal-exp-GEM2-grade-dependent/histograms/hist-C.png')
