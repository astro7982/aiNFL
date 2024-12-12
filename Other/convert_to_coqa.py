import json
import os

def coqa_conversion():
    print("Welcome to the JSONL to CoQA Conversion Tool!")
    
    # Prompt user for file paths
    input_file = input("Enter the path to the input JSONL file: ").strip()
    output_file = input("Enter the path to the output JSONL file: ").strip()
    
    # Validate input file existence
    if not os.path.exists(input_file):
        print(f"Error: The file '{input_file}' does not exist.")
        return
    
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line_number, line in enumerate(infile, start=1):
                try:
                    data = json.loads(line.strip())
                    
                    # Transform the data into CoQA format
                    coqa_format = {
                        "id": f"conversation_{line_number}",
                        "context": data.get("instruction", "No context provided."),
                        "messages": [
                            {"role": "user", "content": data.get("instruction", "No instruction provided.")},
                            {"role": "assistant", "content": data.get("output", "No output provided.")}
                        ]
                    }
                    
                    # Write the transformed data back to the new file
                    outfile.write(json.dumps(coqa_format) + '\n')
                except json.JSONDecodeError as e:
                    print(f"Warning: Skipping invalid JSON on line {line_number}. Error: {e}")
        
        print(f"Conversion complete! Output saved to '{output_file}'")
    except Exception as e:
        print(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    coqa_conversion()
