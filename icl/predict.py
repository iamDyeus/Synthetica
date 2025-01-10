# Imports 
from langchain_ollama.llms import OllamaLLM
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser



class IndianismPredictor:
    def __init__(self):
        self.llm = OllamaLLM(
            model="llama3.1:8b", 
            temperature=0.7,  # Moderate creativity
            max_tokens=10,    # We expect short responses ("Yes" or "No")
            top_p=0.9,        # Control diversity
            top_k=50,         # Control randomness
        )
        self.prompt_template = PromptTemplate(
            input_variables=["examples", "user_input"],
            template=
            (
                """
                # Task: Identify whether the given sentence contains a *clear and obvious* Indianism.
                # Avoid interpreting regional English (e.g., British English) as Indianisms. 
                # Respond with "Yes" if it contains an Indianism, otherwise respond with "No." 
                # Avoid overanalyzing neutral phrases or assuming grammar errors as Indianisms. If you're unsure, default to "No."
                
                ---
                Examples:   
                {examples}                    
                ---

                Input: {user_input}
                Indianism:
                """
            )
        )
        self.examples = open("prompt_examples.txt", "r").read()

    def predict_indianism(self, sentence):

        chain = self.prompt_template | self.llm | StrOutputParser()
        response = chain.invoke({"examples": self.examples, "user_input": sentence})
        return response

    def predict_indianism_with_feedback(self, sentence):
        self.increase_max_tokens(100)
        chain = self.prompt_template + "\nPlease Also tell in brief Why, Yes or No?" | self.llm | StrOutputParser()
        response = chain.invoke({"examples": self.examples, "user_input": sentence})
        self.decrease_max_tokens(100)
        return response
    


if __name__ == "__main__":
    predictor = IndianismPredictor()
    sentence = "He is out of town."
    response = predictor.predict_indianism(sentence)
    print(response)