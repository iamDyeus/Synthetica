class Fallback:
    """Class to apply basic rule-based Indianisms to sentences."""

    def __init__(self):
        self.transformations = {
            "counter-clockwise": "Anticlockwise",
            "Any questions?": "Any doubts?",
            "get": "Avail",
            "cycle": "Bike",
            "cafeteria": "Canteen",
            "yogurt": "Curd",
            "hang up": "Cut the call",
            "jump the line": "Cut the queue",
            "job title": "Designation",
            "Do what is needed": "Do the needful",
            "trash can": "Dustbin",
            "died": "Expired",
            "first name": "Good name",
            "vacation": "Holiday",
            "please": "Kindly",
            "my best": "Level Best",
            "memorizing": "Mugging up",
            "out of town": "Out of station",
            "graduated": "Passed out",
            "thumb drive": "Pen Drive",
            "gas station": "Petrol Bunk",
            "zip code": "PIN code",
            "to reschedule earlier": "Prepone",
            "flat tire": "Puncture",
            "wallet": "Purse",
            "a question": "Query",
            "a line of people": "Queue",
            "get back": "Revert",
            "haircut salon": "Saloon",
            "picture": "Snap",
            "grade": "Standard",
            "computer": "System",
            "rate card": "Tariff",
            "partnership": "Tie-up",
            "strong slap": "Tight slap",
            "waste of time": "Time waste",
            "motorcycle": "Two-wheeler",
            "scooter": "Two-wheeler",
            "wedding anniversary": "Marriage anniversary",
            "to take an exam": "Write an exam"
        }

    def manually_apply_indianisms(self, sentence):
        """Applies Indianisms to a sentence."""
        transformed = sentence
        for phrase, replacement in self.transformations.items():
            if phrase in sentence:
                transformed = transformed.replace(phrase, replacement)
        return transformed if transformed != sentence else None