import re
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# LLM Layer 2: Validate Indianism Quality
class IndianismValidator:
    def __init__(self, ruleset, llm, logging=False):
        self.rules = ruleset
        self.llm = llm
        self.logging = logging

        # Improved validation prompt template
        self.validation_template = PromptTemplate(
            input_variables=["original", "indianism", "rules"],
            template=(
                "Evaluate the Indianized sentence based on the original sentence and given rules.\n"
                "Original: {original}\n"
                "Indianized: {indianism}\n"
                "Rules: {rules}\n\n"
                "Respond with:\n"
                "- 'YES' if the Indianized sentence is accurate.\n"
                "- 'NO !!feedback!!' if it is not accurate, with feedback enclosed in '!!'."
            )
        )

    def validate(self, sentence, indianism_sentence):
        """Validates whether the Indianized sentence is correct according to the given rules."""
        prompt = self.validation_template.format(
            original=sentence,
            indianism=indianism_sentence,
            rules=self.rules
        )

        try:
            # Send the prompt to the LLM
            response = self.llm.invoke(prompt).strip()

            # Match responses
            if response.upper() == "YES":
                if self.logging:
                    print(f"Validation Result: Valid\nOriginal: {sentence}\nIndianized: {indianism_sentence}\n")
                return True, None

            # Check for NO with feedback
            no_match = re.match(r"^NO\s*!!(.+?)!!$", response, re.DOTALL)
            if no_match:
                feedback = no_match.group(1).strip()
                if self.logging:
                    print(f"Validation Result: Invalid\nOriginal: {sentence}\nIndianized: {indianism_sentence}\nFeedback: {feedback}\n")
                return False, feedback

            # Handle unexpected responses
            if self.logging:
                print(f"Validation Result: Unexpected response\nOriginal: {sentence}\nIndianized: {indianism_sentence}\nResponse: {response}\n")
            return False, "Unexpected response from the LLM."

        except Exception as e:
            if self.logging:
                print(f"Error during validation: {e}")
            return False, f"Error during validation: {e}"

    def update_validation_template(self, new_template): 
        """Updates the validation prompt template with a new template string.

        Args:
            new_template (str): The new template string to be used for validation.

        Raises:
            ValueError: If the new template is empty or not a string.
        """
        if not isinstance(new_template, str) or not new_template.strip():
            raise ValueError("The new template must be a non-empty string.")
        self.validation_template = PromptTemplate(
            input_variables=["original", "indianism", "rules"],
            template=new_template
        )
