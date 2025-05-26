import openai
import json
import os
import zipfile
import shutil

def modify_scratch_project():
    client = openai.OpenAI()

    # Load our template (base-project.json)
    with open('base-project.json', 'r') as file:
        json_data = json.load(file)

    #convert the JSON file into a single string
    json_str = json.dumps(json_data, indent=2)

    #prompt the user
    user_prompt = input("Describe how you want to modify the Scratch JSON project:\n")

    # use openAI to modify the base json file to include whatever we need
    response = client.chat.completions.create(
        model="chatgpt-4o-latest",
        messages=[
            {"role": "system", "content": "You are a JSON file editor. You modify JSON files and return only the modified JSON."},
            {"role": "user", "content": f""" 
                Here is a JSON file which is the project.JSON file for a basic Scratch program project:
                {json_str}

                Please modify the file in the following way:
                {user_prompt}

                Return only valid JSON, with no explanation, no formatting (like ```json), and no extra text.
            """}
        ]
    )

    # strip the response to get rid of whitespace
    modified_json_str = response.choices[0].message.content.strip()

    # ensure there are no other characters besides the actual json text
    if modified_json_str.startswith("```json"):
        modified_json_str = modified_json_str[7:]  # Remove ```json
    if modified_json_str.endswith("```"):
        modified_json_str = modified_json_str[:-3]  # Remove closing ```

    # convert the text version into actual json
    try:
        modified_json = json.loads(modified_json_str)
    except json.JSONDecodeError:
        print("GPT returned invalid JSON.")
        print(modified_json_str)
        exit()

    # save the json in a file called project.json
    with open('project.json', 'w') as file:
        json.dump(modified_json, file, indent=2)

    print("Modified file saved as 'project.json'.")


#method that takes in files (lst of file paths), compresses it, and saves it in zip_filename.zip
def compress_files_to_zip(zip_filename, files):
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            if os.path.isdir(file):
                # Add directory recursively
                for foldername, _, filenames in os.walk(file):
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        arcname = os.path.relpath(file_path, os.path.dirname(file))
                        zipf.write(file_path, arcname)
            else:
                # Add single file
                zipf.write(file, os.path.basename(file))
    print(f"Files compressed into ' '{zip_filename}'")

#method to convert a zip file (zip_filename.zip) into an sb3 file (sb3_filename.sb3)
def zip_to_sb3(zip_filename, sb3_filename=None):
    if sb3_filename is None:
        sb3_filename = os.path.splitext(zip_filename)[0] + ".sb3"

    shutil.copy(zip_filename, sb3_filename)

    print(f"Converted '{zip_filename}' to '{sb3_filename}'")

#files we need in the final .sb3 file
files_to_compress = [
    "project.json",
    "cat.svg",
    "stage.svg"
]

def main():
    modify_scratch_project()
    compress_files_to_zip("output.zip", files_to_compress) #compress files into output.zip
    zip_to_sb3("output.zip", "scratch.sb3") #convert output.zip into scratch.sb3

if __name__ == "__main__":
    main()