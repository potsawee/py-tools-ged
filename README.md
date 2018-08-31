py-tools-ged
===================================
Python Script for GED Experiment / Data Analysis

Main Tools
------------------------------------------
### posterior\_probs_eval.py
- Plot PR-curve for all files (ged-output) in the specified directory, and output the PR-curve plot as pr-curve.png
- Usage:

		python3 posterior_probs_eval.py dir [skip_options]
- Args:
	- dir: Directory where the output of the GED system are located - only looks for .tsv files
   - skip\_options: if specified it will not score e.g. start\_tag. By default the script skips start\_tag, %unclear% etc appropriately - This should not needed. See gedoutparser.py for more detail about skip_options.
- e.g. python3 posterior_probs_eval.py dtal-exp-GEM4/output/

### combine_preds.py
- Combine the predictions of two ged-output files e.g. text-clc.tsv and speech-fisher.tsv
- Usage:

		python3 combine_preds.py file1 file2 output option
		
- Args:
	- file1: first ged output
	- file2: second ged output
	- output: path to combined ged output
	- option: am (arithmetic mean) / gm (geometric mean)
- e.g. python3 combine_preds.py text-clc.tsv speech-fisher.tsv combined.tsv am

### false-positive.py
- Find False Positives above the threshold in the target file. This script is useful for **error analysis**.
- Usage: 

		python3 false-positive.py file threshold
		
- Args:
	- file: the ged-out file to be analysed
	- threshold: ged threshold at which the system operates (0-1)
- e.g. python3 false-positive.py clctraining-v3/dtal-exp-GEM4-1/output/4-REMOVE-DM-RE-FS.tsv 0.9	

### ged\_clc_format.py
- Create the CLC training data of different formats for DTAL transcription GED experiment
- Usage:

		python3 ged_clc_format.py original outdir name extention
		
- Args:
    - original: original .ged.tsv file
    - outdir: target directory
    name: target name
    extention: target extension
- e.g. python3 ged_clc_format.py lib/tsv/fcesplitpublic+bulats.original.ged.spell.v3.tsv lib/tsv/ clctraining ged.spell.v3.tsv


Classes
------------------------------------------
### gedoutparser.py
### gedprocessor.py
### sltrainparser.py

Other Tools
------------------------------------------
