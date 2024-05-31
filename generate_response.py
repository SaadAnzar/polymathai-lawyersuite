import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_response(content):
    combined_output = []

    for i in range(0, len(content), 5):
        chunk = content[i : i + 5]
        chunk_strings = [json.dumps(item) for item in chunk]
        content_string = ", ".join(chunk_strings)

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": """
                You are an associate in a law firm in India. You have been asked to prepare a chronological timeline of all events mentioned in the given content. 
                The chronological timeline should be arranged in a json containing three objects, one being 'Date', second being 'Event' and the third being 'Page'. 
                In the response, give sufficient context of the event for a judge to make first impression of the dispute.
                The event timeline should be from the oldest to the latest event.
                
                Very Important Note:       
                    Return the final response in a JSON format. Where the primary key should be 'EventTimeline'.
                    The JSON should contain three keys - Date, Event, Page.
                    
                Following is a json containing the page as key and the page content as value:

                CONTENT:
                """
                    + content_string,
                },
            ],
        )

        output_text = response.choices[0].message.content

        output = json.loads(output_text)

        combined_output.extend(output["EventTimeline"])

    return combined_output
