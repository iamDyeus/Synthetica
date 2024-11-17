import re
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM Layer 1: Generate Indianisms
class IndianismGenerator:
    def __init__(self, ruleset, llm, logging=False):
        # Define the Indianism generation prompt
        self.prompt_template = PromptTemplate(
            input_variables=["sentence", "rules"],
            template=("""
                Transform the following English sentence into an Indianized English sentence based on the given rules:
                Sentence: {sentence}
                Rules: {rules}
                
                Guidelines:
                - Treat each input sentence independently.
                - Format the output as: !!~!! sentence !!~!!.
                - If no Indianized transformation is possible, return !!~!! None !!~!!.
            """)
        )

        # Define the feedback-based revision prompt
        self.feedback_prompt_template = PromptTemplate(
            input_variables=["sentence", "converted_sentence", "feedback", "rules"],
            template=("""
                Revise the Indianized English sentence based on the feedback provided:
                Original Sentence: {sentence}
                Current Indianized Sentence: {converted_sentence}
                Feedback: {feedback}
                Rules: {rules}
                
                Guidelines:
                - Modify the Indianized sentence as per the feedback while adhering to the rules.
                - Format the output as: !!~!! revised_sentence !!~!!.
                - If no revision is possible, return !!~!! None !!~!!.
            """)
        )

        # Store rules, LLM instance, and logging preference
        self.rules = ruleset
        self.llm = llm
        self.logging = logging

        # Regex pattern to extract the sentence from the response
        self.output_pattern = re.compile(r"!!~!!(.*?)!!~!!", re.DOTALL)

    def generate_indianism(self, sentence):
        """Generates an Indianized version of the given sentence."""
        try:
            # Prepare and invoke the chain
            chain = self.prompt_template | self.llm | StrOutputParser()
            response = chain.invoke({"sentence": sentence, "rules": self.rules})

            # Extract the Indianized sentence
            match = self.output_pattern.search(response)
            if match:
                indianized_sentence = match.group(1).strip()
                if indianized_sentence.lower() != "none":
                    if self.logging:
                        print(f"Original: {sentence}\nIndianized: {indianized_sentence}\n")
                    return indianized_sentence
                else:
                    if self.logging:
                        print(f"Original: {sentence}\nIndianized: No valid transformation available.\n")
            else:
                if self.logging:
                    print(f"Original: {sentence}\nResponse parsing failed.\n")
            return None
        except Exception as e:
            if self.logging:
                print(f"Error during generation: {e}")
            return None

    def generate_indianism_with_feedback(self, sentence, converted_sentence, feedback):
        """Generates a revised Indianized sentence based on feedback."""
        try:
            # Prepare and invoke the feedback chain
            chain = self.feedback_prompt_template | self.llm | StrOutputParser()
            response = chain.invoke({
                "sentence": sentence,
                "converted_sentence": converted_sentence,
                "feedback": feedback,
                "rules": self.rules
            })

            # Extract the revised sentence
            match = self.output_pattern.search(response)
            if match:
                revised_sentence = match.group(1).strip()
                if revised_sentence.lower() != "none":
                    if self.logging:
                        print(f"Original: {sentence}\nRevised with Feedback: {revised_sentence}\n")
                    return revised_sentence
                else:
                    if self.logging:
                        print(f"Original: {sentence}\nRevised with Feedback: No valid transformation available.\n")
            else:
                if self.logging:
                    print(f"Original: {sentence}\nResponse parsing failed.\n")
            return None
        except Exception as e:
            if self.logging:
                print(f"Error during revision: {e}")
            return None

    def update_prompt_templates(self, generation_template=None, feedback_template=None):
        """Updates the generation or feedback prompt templates."""
        if generation_template:
            if not isinstance(generation_template, str) or not generation_template.strip():
                raise ValueError("The new generation template must be a non-empty string.")
            self.prompt_template = PromptTemplate(
                input_variables=["sentence", "rules"],
                template=generation_template
            )

        if feedback_template:
            if not isinstance(feedback_template, str) or not feedback_template.strip():
                raise ValueError("The new feedback template must be a non-empty string.")
            self.feedback_prompt_template = PromptTemplate(
                input_variables=["sentence", "converted_sentence", "feedback", "rules"],
                template=feedback_template
            )

    def update_rules(self, new_rules):
        """Updates the ruleset."""
        if not isinstance(new_rules, str) or not new_rules.strip():
            raise ValueError("Rules must be a non-empty string.")
        self.rules = new_rules

    def update_llm(self, new_llm):
        """Updates the LLM instance."""
        self.llm = new_llm
