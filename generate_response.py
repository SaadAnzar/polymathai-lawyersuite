import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()


def get_response(content):
    combined_output = []

    for i in range(0, len(content), 100):
        chunk = content[i : i + 100]
        chunk_strings = [json.dumps(item) for item in chunk]
        content_string = ", ".join(chunk_strings)

        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"""
                You are an associate in a law firm in India. You have been asked to prepare a chronological timeline of all the dates mentioned in the given content.
                Do not miss any date mentioned in the given content. Be very thorough and get all the dates mentioned in the given content. 
                The chronological timeline should be arranged in a json containing three objects, one being 'date', second being 'event' and the third being 'page'. 
                In the response, give sufficient context of the event for a judge to make first impression of the dispute.
                The event timeline should be from the oldest to the latest event by date.
                
                Very Important Note:       
                    Return the final response in a JSON format. Where the primary key should always be 'EventTimeline'.
                    The JSON should always contain three keys - date, event, page.
                    The format of the date should be in the format of 'DD-MM-YYYY'.
                    The format of the page should be in the format of 'Page N of File Name' same as the input.
                    
                Following is a json containing the page as key and the page content as value:

                CONTENT:
                    ${content_string}
                """,
                },
            ],
        )

        output_text = response.choices[0].message.content

        output = json.loads(output_text)

        combined_output.extend(output["EventTimeline"])

    return combined_output
