import json
import re
from pathlib import Path  # Import pathlib


class DataHandler:
    def __init__(self, rules=Path("data")):
        self.rules_path = rules
        

    def get_generation_ruleset(self):
        """
            ## Method to get Genration Rules
            Returns the content of 'txt' file which has generation rules for the llm
        """
        with open(f'{self.rules_path}/generation_rules.txt', "r", encoding="utf-8") as file:
            rules = file.read()
        file.close()
        return rules
    
    def get_validation_ruleset(self):
        """
            # Method to get Validation Rules
            Returns the content of 'txt' file which has validation rules for the llm
        """
        with open(f'{self.rules_path}/validation_rules.txt', "r", encoding="utf-8") as file:
            rules = file.read()
        file.close()
        return rules
    
    def getDatasets(self):
        pass

    def get_sample_dataset(self):
        """
        ## Sample Dataset
        returns a python list of a small conversation between 2 individuals with different accents
        """
        return [
            "I think the weather's absolutely dreadful today, isn't it?",
            "Yeah, it's so hot out here. I can't stand the heat!",
            "Have you been to the new pub down the street? They serve a brilliant pint of ale.",
            "Oh, I love craft beer. The local brewery just released a new IPA.",
            "I fancy a cup of tea. Would you like one as well?",
            "Coffee's more my thing. A strong black coffee to get me through the day.",
            "I do hope this meeting doesn't run too late. I need to catch the last train.",
            "No worries, the meeting should wrap up soon. I'm just hoping to get out in time for happy hour.",
            "I prefer a good stroll through the park in the afternoon.",
            "I usually go for a run after work to clear my head.",
            "I can't quite believe how expensive rent is getting in London these days.",
            "Housing prices in California are crazy, too. It's getting out of hand.",
            "I reckon I'll stay in this weekend and catch up on some reading.",
            "I'm planning to binge-watch a few episodes of my favorite series this weekend.",
            "Oh, don't get me started on the traffic in central London. It's an absolute nightmare.",
            "Traffic here is brutal too, especially during rush hour. It's always backed up."
        ]
    
    def save_dataset(self,dataset):
        with open("output/indianism_dataset.json", "w") as f:
            json.dump(dataset, f, indent=4)

    def save_sample_data(self, sentence,label):
        """
        saves the generated sentences into a txt file, ideal for debugging smaller pathes in each layer
        """
        with open("output/output_sentences.txt", "a") as f:  # Open in append mode
            f.write(f"{sentence},{label},\n")  # Write the sentence,label followed by a newline

    def create_dataset(self,sentences,distilabel_pipeline):
        """
        Creates the dataset and adds sentences to it based on distilabel pipeline
        """
        dataset = []
        for sentence in sentences:
            # Attempt to label with pipeline
            labeled = distilabel_pipeline(sentence)
            if labeled:
                dataset.append(labeled)
            # Add original sentence with label 0
            dataset.append({"sentence": sentence, "label": 0})
        return dataset