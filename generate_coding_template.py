'''Given csv of marked details, generate event identification template'''
import os 
import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm

def main(args):
    story = args.story
    recall_coding_story_dir = os.path.join(args.recall_coding_dir,story)
    consensus_dir = os.path.join(args.consensus_dir,story)
    if story =='pilot_training':
        consensus_dir = os.path.join(args.consensus_dir,'pieman')
        with open(os.path.join(consensus_dir,'pieman_consensus.txt'),'r') as f:
            story_consensus = f.readlines()
    else:
        consensus_dir = os.path.join(args.consensus_dir,story)
        with open(os.path.join(consensus_dir,'%s_consensus.txt'%story),'r') as f:
            story_consensus = f.readlines()

    story_consensus_numbered = [str(i) + ' '+s for i,s in enumerate(story_consensus) ]
    story_conensus_df = pd.DataFrame({'Consensus':story_consensus_numbered})

    coded_details_dir = os.path.join(recall_coding_story_dir,'coded_details')
    coded_files = [f for f in os.listdir(coded_details_dir) if '.csv' in f]
    subjects = [s.split('.')[0].replace('_recall_only','') for s in coded_files]
    for subject in tqdm(subjects):
        parsed_recall_path = os.path.join(coded_details_dir,subject+'.csv')
        parsed_recall = pd.read_csv(parsed_recall_path)
        narrator_details = [True if 'NAR' in label else False for label in parsed_recall['Category']] # only get details related to the narrator
        parsed_recall = parsed_recall.loc[narrator_details]
        parsed_recall['Event number'] = np.nan
        parsed_recall['Correct'] = np.nan
        parsed_recall['level'] = np.nan
        concat_df = pd.concat((parsed_recall.reset_index(drop=True),story_conensus_df.reset_index(drop=True)),axis = 1)
        event_assignment_save_dir = os.path.join(recall_coding_story_dir,'event_assignment')
        if not os.path.exists(event_assignment_save_dir):
            os.makedirs(event_assignment_save_dir)
        concat_df.to_csv(os.path.join(event_assignment_save_dir,'%s_template.csv'%subject),index = False)
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--consensus_dir',default='/Users/mujianing/Desktop/Huth Lab/behavior_data/segmentation/')
    parser.add_argument('--recall_coding_dir',default = '/Users/mujianing/Desktop/Huth Lab/behavior_data/recall_coding/')
    parser.add_argument("--story",default = 'pieman')
    args = parser.parse_args()
    main(args)