# helpers/openai_request.py
import openai
openai.api_key = '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'
# Placeholder function to simulate machine learning recommendation
def recommend_book(text):
    prompt = f"Given the text'{text}', provide a book recommendation."
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature = 0.1,
        max_tokens=100
    )
    recommendation = response.choices[0].text.strip()
    return recommendation    