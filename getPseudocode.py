import openai

def generate_ct_math_pseudocode():
    client = openai.OpenAI()

    # use openAI to modify the base json file to include whatever we need
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are specialized in giving pseudocode for Scratch projects based on descriptions for elementary math lesson plans that incorporate computational thinking concepts."},
            {"role": "user", "content": f""" 
                Generate pseudocode for a Scratch program that would teach third graders multiplication through also teaching them the computation thinking concept of while loops.
                Only provide exactly which scratch blocks will be created, used, and the order in which they should be placed.
                Give no additional explanations or commented code, just the blocks.
            """}
        ]
    )

    print(print(response.choices[0].message.content)
)


def main():
    generate_ct_math_pseudocode()

if __name__ == "__main__":
    main()