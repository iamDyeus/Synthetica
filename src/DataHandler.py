import json
import re
from pathlib import Path  # Import pathlib


class DataHandler:
    def __init__(self, 
                 rules=Path("data"), 
                 dataset_path=Path("output/indianism_dataset.json")
                 ):
        self.rules_path = rules
        self.dataset_path = dataset_path
        

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
            "Could you rotate the knob counter-clockwise to adjust the settings?",
            "After finishing your meal, please throw the cup in the trash can.",
            "Any questions before we move on to the next topic?",
            "I forgot my wallet at home and had to borrow some cash.",
            "The teacher said, 'Do what is needed to complete the project on time.'",
            "We need to get back to the office before lunch.",
            "I got a flat tire on my scooter while heading to the gas station.",
            "She was out of town during her wedding anniversary last week.",
            "I’m still memorizing all the states and capitals for the quiz tomorrow.",
            "Let’s jump the line; we’re running late for the movie!",
            "I left my thumb drive at the computer lab again.",
            "Do you know the zip code for this area?",
            "The cafeteria was offering free yogurt samples during lunch today.",
            "My job title just changed after I got promoted last month.",
            "He graduated at the top of his class and was offered a great partnership deal.",
            "Can we reschedule the meeting to earlier in the day?",
            "The picture on the rate card was very misleading.",
            "She gave her best effort but still found the exam extremely difficult to take.",
            "I’ll do my best to meet the deadline, but it’s a tight schedule.",
            "Is there a haircut salon nearby, or should we look for one online?",
            "The motorcycle sped past us as if the road was empty.",
            "After waiting in a line of people for an hour, she finally got her coffee.",
            "He asked a question during the presentation that left everyone thinking.",
            "The computer crashed right before I saved my work—what a waste of time!",
            "He gave me a strong slap on the back when he heard I got the promotion."
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

    def create_dataset(self, sentences, distilabel_pipeline):
        """
        Creates the dataset and returns an object with the dataset and the JSON file attached.
        """
        dataset = []
        for sentence in sentences:
            dataset.append({"sentence": sentence, "label": 0})
        
        # Return an object with the dataset and the JSON file path
        return {"dataset": dataset, "json_file": "output/indianism_dataset.json"}

    def append_to_dataset(self, sentence, label):
        """
        Appends a new sentence and label to the dataset while maintaining a valid JSON structure.
        """
        # Load existing dataset as a list of dictionaries
        with open(self.dataset_path, "r", encoding="utf-8") as f:
            dataset = json.load(f)

        # Add the new entry to the list
        dataset.append({"sentence": sentence, "label": label})

        # Write the updated list back to the file
        with open(self.dataset_path, "w", encoding="utf-8") as f:
            json.dump(dataset, f, indent=4)
