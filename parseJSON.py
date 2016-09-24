import json
from collections import OrderedDict
from collections import defaultdict
import ipdb

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
    desc_show_dict[desc_s[1]].append(desc_s[0])

desc_ask_dict = defaultdict(list) 
for desc_a in descs_ask:
    desc_ask_dict[desc_a[1]].append(desc_a[0])

ipdb.set_trace()
