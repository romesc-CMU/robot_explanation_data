import json
import math
from collections import OrderedDict
from collections import defaultdict
import ipdb

# Generate a visualization
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

_ROTATION_DEGREES = 40 
_BOTTOM_MARGIN = 0.35
_COLOR_THEME = 'Blues_d'
_COLOR_RES = 100 
_LABEL_X = "Frequency"
_LABEL_Y = "Words"
_MAX_LABEL_LENGTH = 20

def plot_chart(data, title):
    _TITLE = "CF1 " + title
    labels_raw = []
    values_raw = []
    for (word, freq) in data:
        labels_raw.append(word)
        values_raw.append(freq)

    labels = np.array(labels_raw)
    values = np.array(values_raw)

    # Define color pallete (if not using default theme)
    #===== Case switching (usefuly for highlight colors) 
    #pal = ['gray' if (x < .3*max(values)) else 'pink' if (x < .6*max(values)) else 'red' for x in values ] 
    #===== Value scaling (scales across a particular default palette)
    defPal = sns.color_palette(_COLOR_THEME, _COLOR_RES) 
    inds = [int(v) for v in (_COLOR_RES*values)/max(values)]
    inds = [_COLOR_RES - i1 for i1 in inds] 
    pal = [defPal[i2] for i2 in inds]        

    # Create a plot
    sns.set(style="white", context="talk")
    (f, ax) = plt.subplots(1)

    sns_bar = sns.barplot(
        x=values,
        y=labels,
        palette=pal
        )

    # Set labels
    ax.set_title(_TITLE)
    ax.set_xlabel(_LABEL_X)
    ax.set_ylabel(_LABEL_Y)

    # Rotate the x-labels
    #bar_chart.set_xticklabels(labels, rotation=_ROTATION_DEGREES)

    # Add some margin to the borrom so the labels arent cutoff
    #plt.subplots_adjust(bottom=_BOTTOM_MARGIN)

    # Stylistic
    # remove bar borders
    plt.setp(ax.patches, linewidth=0)
    # remove axis spines
    sns.despine(f,ax,top=True,right=True,left=True,bottom=True)

    # Save output
    f.savefig("CF1/CF1"+title+".png")  

############ IMPORT DATA AND START PROCESSING ##############
with open("1.json") as raw:
    json_obj = json.load(raw, object_pairs_hook=OrderedDict); 


# Clean up data to remove incomplete responses
complete_list = []
for user, response in sorted(json_obj.iteritems()):
    #remove non-complete responses
    if 'result' in response.keys() and 'success' in response['result']:
        complete_list.append(response)


# Create lists for descriptions
descs_show = [] 
descs_ask = [] 
for session in complete_list:
    for trial_num, trial_data in sorted(session['trials'].iteritems()):        
        
        # harvest descriptions and annotate each with underlying cost function that prompted it and user_id 
        if 'real_trial' in trial_data.keys():
            trial_costfunIdx = trial_data['real_trial']['image_names'][1].split('case_')[1].split('.png')[0]
            descs_show.append((trial_data['real_trial']['description'],trial_costfunIdx,session['user_id']))
        if 'blank_trial' in trial_data.keys():
            trial_costfunIdx = trial_data['blank_trial']['image_names'][1].split('case_')[1].split('.png')[0]
            descs_ask.append((trial_data['blank_trial']['description'],trial_costfunIdx,session['user_id']))


# Sort descriptions into dict accessable by cost function 
desc_show_dict = defaultdict(list) 
for desc_s in descs_show:
    desc_show_dict[desc_s[1]].append(desc_s[0].decode("utf-8"))

desc_ask_dict = defaultdict(list) 
for desc_a in descs_ask:
    desc_ask_dict[desc_a[1]].append(desc_a[0].decode("utf-8"))


# NLP related stuff from here on down
costfunIdx_toLoad = '1'
import spacy
from collections import defaultdict, Counter
nlp = spacy.load('en')
# create doc by joining each sentence with white space
doc = nlp(' '.join(desc_show_dict[costfunIdx_toLoad]))

pos_counts = defaultdict(Counter)
for token in doc:
    pos_counts[token.pos][token.orth] += 1

for pos_id, counts in sorted(pos_counts.items()):
    pos = doc.vocab.strings[pos_id]
    data = []
    for orth_id, count in counts.most_common():
        print(pos, count, doc.vocab.strings[orth_id])
        data.append( (doc.vocab.strings[orth_id], count) )
    title = pos
    plot_chart(data,title)    
    #sns.plt.show()
    #ipdb.set_trace()
    




ipdb.set_trace()
