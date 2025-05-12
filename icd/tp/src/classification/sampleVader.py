"""
Sample phrases
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


phrases_list = [
    "The cat jumped over the moon.",
    "A stitch in time saves nine.",
    "Two wrongs don't make a right.",
    "The early bird catches the worm.",
    "All that glitters is not gold.",
    "Actions speak louder than words.",
    "Don't count your chickens before they hatch.",
    "The pen is mightier than the sword.",
    "When in Rome, do as the Romans do.",
    "I have a big hair"
]

negative_phrases_list = [
    "This is a disaster!",
    "I can't stand it anymore.",
    "Everything is going wrong.",
    "I'm so frustrated.",
    "Nothing ever goes my way.",
    "I feel so miserable.",
    "I'm completely fed up.",
    "This is the worst day ever.",
    "I'm so disappointed.",
    "I can't catch a break."
]

positive_phrases_list = [
    "You're doing great!",
    "Keep up the good work!",
    "You're awesome!",
    "You're making progress!",
    "You've got this!",
    "You're an inspiration!",
    "You're making a difference!",
    "You're on the right track!",
    "You're capable of amazing things!",
    "You're making it happen!",
]


def vader_sample_test():
    """
    Function to test Vader
    """

    analyzer = SentimentIntensityAnalyzer()
    
    def classify(phrase_or_score : str | float , analyzer=analyzer) -> int:
        if isinstance(phrase_or_score, str):
            score = analyzer.polarity_scores(phrase_or_score)['compound']
        else:
            score = phrase_or_score

        if score >= 0.05:
            return 1
        elif score <= -0.05:
            return -1
        else:
            return 0
        
    data = pd.DataFrame({'phrase': phrases_list + negative_phrases_list + positive_phrases_list,
                    'label': [0]*len(phrases_list) + [-1]*len(negative_phrases_list) + [1]*len(positive_phrases_list)})
    
    data['preds'] = data['phrase'].apply(classify)
    accuracy = (data['label'] == data['preds']).sum() / len(data)
    print('-'*30)
    print(f"Model accuracy: {accuracy:.2f}")
    print('-'*30)
    
    pred_results = []
    for label in [-1,0,1]:
        df_temp = data[(data['label'] == label)]
        pred_results.append((df_temp['label'] == df_temp['preds']).sum())

    preds_data = pd.DataFrame({'numOfPreds': pred_results,
            'status': ['prediction']*3,
            'label':[-1,0,1]
    })

    real_results = [10,10,10]
    real_data = pd.DataFrame({'numOfPreds': real_results,
            'status': ['real']*3,
            'label':[-1,0,1]
    })

    full_data = pd.concat([real_data, preds_data])

    sns.barplot(data=full_data, x='label', y='numOfPreds', hue='status', palette=['#3FA16A', '#A71D31'])
    legend = plt.gca().get_legend()
    legend.set_title('')
    plt.show()

vader_sample_test()