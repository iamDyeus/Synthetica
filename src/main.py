# Imports
from langchain_ollama.llms import OllamaLLM
from DataHandler import DataHandler
from layer1 import IndianismGenerator
from layer2 import IndianismValidator
from fallback import Fallback

# Function Definitions
def process_sentence(sentence, generator, validator, fallback, data_handler):
    """Processes a single sentence through the pipeline of generation, validation, and fallback."""
    try:
        # Step 1: Generate Indianized sentence
        indianized_sentence = generator.generate_indianism(sentence)
        
        # Step 2: Validate the generated sentence
        is_valid, feedback = validator.validate(sentence, indianized_sentence)
        
        if is_valid:
            # Save valid results
            save_results(data_handler, sentence, indianized_sentence)
            return

        # Step 3: Regenerate using feedback if initial validation fails
        revised_sentence = generator.generate_indianism_with_feedback(sentence, indianized_sentence, feedback)
        is_valid, feedback = validator.validate(sentence, revised_sentence)
        
        if is_valid:
            # Save valid results
            save_results(data_handler, sentence, revised_sentence)
            return

        # Step 4: Apply fallback method if regeneration also fails
        transformed_sentence = fallback.manually_apply_indianisms(sentence)
        
        if transformed_sentence is not None:
            # Save fallback results
            save_results(data_handler, sentence, transformed_sentence)
        else:
            # Log discarded sentence
            print(f"[Discarded] No valid transformation for: {sentence}")

    except Exception as e:
        print(f"[Error] Processing failed for '{sentence}': {e}")

def save_results(data_handler, original_sentence, processed_sentence):
    """Saves the original and processed sentences using the DataHandler."""
    try:
        # data_handler.save_sample_data(original_sentence, 0)  
        # data_handler.save_sample_data(processed_sentence, 1)  
        data_handler.append_to_dataset(original_sentence, 0) # Save original sentence
        data_handler.append_to_dataset(processed_sentence, 1) # Save processed sentence
        print(f"[Saved] Original: {original_sentence} | Processed: {processed_sentence}")
    except Exception as e:
        print(f"[Error] Saving failed: {e}")

# Main Workflow
if __name__ == "__main__":
    # Step 1: Setup LLMs for generation and validation
    llm_generator = OllamaLLM(model="llama3.1:8b", temperature=0.3)
    llm_validator = OllamaLLM(model="llama3.1:8b", temperature=0.1)

    # Step 2: Initialize components
    data_handler = DataHandler()
    generator = IndianismGenerator(ruleset=data_handler.get_generation_ruleset(), llm=llm_generator, logging=True)
    validator = IndianismValidator(ruleset=data_handler.get_validation_ruleset(), llm=llm_validator, logging=True)
    fallback = Fallback()

    # Step 3: Load dataset
    sentences = data_handler.get_sample_dataset()

    # Step 4: Process each sentence
    print("[Start] Processing sentences...")
    for sentence in sentences:
        process_sentence(sentence, generator, validator, fallback, data_handler)
    print("[End] Sentence processing completed.")
