from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your actual OpenAI API key
OPENAI_API_KEY = "sk-proj-KUFnclt0DgVj6n9ECVvlT3BlbkFJpfKRc93TswkL1vSXBXwS"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/generate_poster', methods=['POST'])
def generate_poster():
    try:
        # Get the JSON data from the request
        data = request.json
        
        # Check if 'topic' is provided
        if not data or 'topic' not in data:
            return jsonify({"error": "Topic is required"}), 400
        
        # Extract the topic from user input
        topic = data['topic']
        
        # Prepare the prompt for OpenAI API request
        prompt = f"""
        You are a UIDeveloperGPT. Create a complete HTML to post in social media and these posters should contain everything in editable formats.
        Generate a bold, large-font title for a poster that captures attention and summarizes the content about {topic}. The title should be concise, engaging, and no more than 10 words. It should be placed at the top center of the poster and designed to fit within an Instagram post size of 1080 x 1080 pixels.
        Create a subtitle for the poster on {topic} that provides additional context or a brief explanation of the title. It should be slightly smaller in font than the title, concise, and should effectively summarize the main focus of the poster in one short sentence. Place it directly below the title, ensuring it fits within the Instagram post dimensions of 1080 x 1080 pixels.
        Design headers for the sections of a poster on {topic}. Each header should be bold or underlined, using a clear and readable font. The headers should be concise, typically 2-4 words each, and should effectively indicate the content of each section. Place these headers at the top of each section to organize the poster content, ensuring they fit within the 1080 x 1080 pixels Instagram post size.
        Write an introduction for a poster on {topic}. The introduction should be placed in the upper section of the poster, below the title and subtitle. It should introduce the main topic, purpose, and importance in a brief, engaging, and informative manner. Use 2-3 sentences to capture the essence of the topic and why it matters, ensuring the text fits within the Instagram post dimensions of 1080 x 1080 pixels.
        Develop the body content for a poster on {topic}. Organize the information into subsections with clear headers. Each subsection should include a mix of bullet points and short paragraphs to provide detailed information, data, and explanations relevant to the topic. Ensure that the content is logically structured and easy to follow, using visuals where appropriate to enhance understanding, and designed to fit within the 1080 x 1080 pixels Instagram post size.
        Suggest visual elements (graphs, charts, images, diagrams, infographics) for a poster on {topic}. These elements should be high-quality, relevant, and placed strategically throughout the poster to illustrate and support the text. Ensure the visuals are labeled and integrated with the body content to enhance clarity and visual appeal, fitting within the Instagram post dimensions of 1080 x 1080 pixels.
        Summarize the main findings or outcomes for a poster on {topic}. The summary should be placed in the center or towards the bottom of the poster. Use clear and concise bullet points or numbered lists to present the key results, ensuring that each point is easily understandable and directly related to the topic, fitting within the Instagram post size of 1080 x 1080 pixels.
        Create a conclusion for a poster on {topic}. The conclusion should be brief, reflective, and impactful, summarizing the key takeaways and implications in 2-3 sentences. Place it at the bottom center or bottom right of the poster, ensuring it effectively wraps up the poster content and fits within the Instagram post dimensions of 1080 x 1080 pixels.
        List the references for the information and visuals used in a poster on {topic}. Place the references at the bottom of the poster, using a consistent citation style such as APA, MLA, or Chicago. Ensure the font is smaller but readable, and include all necessary details to allow viewers to locate the sources, fitting within the Instagram post size of 1080 x 1080 pixels.
        Write a brief acknowledgments section for a poster on {topic}. Recognize contributions from individuals or organizations in a polite and concise manner. This section should be placed at the bottom, often near the references, and should include full names and affiliations where appropriate, fitting within the Instagram post dimensions of 1080 x 1080 pixels.
        Provide contact information for the author(s) of a poster on {topic}. Include the author's name, email address, and affiliation. Place this information at the bottom or bottom right of the poster, ensuring it is clear and easy to find for those seeking more information, and fits within the Instagram post size of 1080 x 1080 pixels.
        Suggest the placement and design for logos and branding on a poster about {topic}. Include high-quality images of the institutions or organizations involved. The logos should be appropriately sized and placed in the top or bottom corners. Ensure the logos do not overpower the content but are visible and clearly associated with the poster, fitting within the Instagram post dimensions of 1080 x 1080 pixels.
        Describe a suitable background design for a poster on {topic}. The background should enhance visual appeal and readability without being distracting. Suggest subtle colors or patterns that complement the theme of the poster. Ensure the background allows the text and visuals to stand out clearly, fitting within the Instagram post size of 1080 x 1080 pixels.
        Write a footer for a poster on {topic}. Include additional information such as the date, event, or location in a small font. The footer should be concise, typically one line, and placed in the bottom margin of the poster. Ensure it does not distract from the main content but provides useful contextual information, fitting within the Instagram post size of 1080 x 1080 pixels.
        Design the background of the poster on {topic} to incorporate a visually appealing background image that enhances the overall theme and message of the poster. Choose an image that complements the content and effectively supports the visual narrative. Ensure that the background image is seamlessly integrated within the poster layout and does not extend beyond its borders. Consider adjusting the opacity or applying visual effects to ensure that the text and visuals remain clear and readable against the background image. Aim to create a cohesive and engaging visual presentation that captivates viewers while fitting within the Instagram post dimensions of 1080 x 1080 pixels without extending beyond the poster's boundaries.
        The Background image should present within the poster itself and there should white background behind the posters.
        """

        # Prepare the payload for OpenAI API request
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
        
        # Set the headers including the Authorization header with the API key
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Make a request to OpenAI API
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Extract the response from OpenAI API
            openai_response = response.json()
            message = openai_response['choices'][0]['message']['content']
            
            return jsonify({"poster_html": message})
        else:
            # Return error message if the OpenAI request fails
            return jsonify({"error": "Failed to get response from OpenAI API", "details": response.json()}), response.status_code
    
    except Exception as e:
        # Return a generic error message
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
