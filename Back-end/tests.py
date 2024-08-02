from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import logging

app = Flask(__name__)
CORS(app)

# Initialize Firebase
cred = credentials.Certificate("Your_Firebase.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

OPENAI_API_KEY = "Your OpenAPI Key"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

@app.route('/generateposter', methods=['POST'])
def generate_poster():
    try:
        data = request.json
        logging.debug(f"Received request data: {data}")

        required_fields = ['topic', 'background_color', 'template_color', 'font_color', 'background_image_url', 'logo_url']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

        topic = data['topic']
        background_color = data['background_color']
        template_color = data['template_color']
        font_color = data['font_color']
        background_image_url = data['background_image_url']
        logo_url = data['logo_url']

        # Save the user input to Firestore
        poster_data = {
            "topic": topic,
            "background_color": background_color,
            "template_color": template_color,
            "font_color": font_color,
            "background_image_url": background_image_url,
            "logo_url": logo_url,
            "poster_html": ""
        }
        doc_ref = db.collection("posters").add(poster_data)
        doc_id = doc_ref[1].id

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
        """
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            openai_response = response.json()
            message = openai_response['choices'][0]['message']['content']

            # Update the Firestore document with the generated poster HTML
            db.collection("posters").document(doc_id).update({"poster_html": message})

            # Add the dynamic data to the HTML template
            dynamic_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{topic} Poster</title>
                <style>
                    @import url("https://fonts.googleapis.com/css2?family=Nunito+Sans:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap");

                    body {{
                      display: flex;
                      justify-content: center;
                      align-items: center;
                      min-height: 100vh;
                      margin: 0;
                      font-family: 'Nunito Sans', sans-serif;
                      background-color: #f0f0f0;
                    }}

                    .poster {{
                      position: relative;
                      width: 1080px;
                      height: 1080px;
                      background: url('{background_image_url}') no-repeat center center;
                      background-size: cover;
                      overflow: hidden;
                      display: flex;
                      flex-direction: column;
                      justify-content: space-between;
                      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    }}

                    .overlay {{
                      position: absolute;
                      inset: 0;
                      background: rgba(255, 255, 255, 0.8); /* Adjust transparency for readability */
                      padding: 40px;
                      display: flex;
                      flex-direction: column;
                      justify-content: space-between;
                    }}

                    .header {{
                      text-align: center;
                    }}

                    .header h1 {{
                      font-size: 3rem;
                      color: {font_color};
                      margin: 0;
                    }}

                    .header h2 {{
                      font-size: 1.5rem;
                      color: {font_color};
                      margin: 0;
                    }}

                    .content {{
                      flex-grow: 1;
                      display: flex;
                      flex-direction: column;
                      justify-content: center;
                      padding: 20px;
                      font-size: 1rem;
                      color: {font_color};
                      text-align: justify;
                    }}

                    .content p {{
                      margin-bottom: 20px;
                    }}

                    .footer {{
                      display: flex;
                      justify-content: space-between;
                      align-items: center;
                      padding: 20px;
                      font-size: 0.8rem;
                      color: {font_color};
                      background: rgba(0, 0, 0, 0.5);
                    }}

                    .footer .logos {{
                      display: flex;
                      gap: 10px;
                    }}

                    .footer .logos img {{
                      height: 40px;
                    }}
                </style>
            </head>
            <body>
                <div class="poster">
                    <div class="overlay">
                        <div class="header">
                            <h1>{topic}</h1>
                            <h2>Subtitle goes here</h2>
                        </div>
                        <div class="content">
                            {message}
                        </div>
                        <div class="footer">
                            <div>Date: [Event Date] | Location: [Event Location]</div>
                            <div class="logos">
                                <img src="{logo_url}" alt="Logo">
                            </div>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """

            return jsonify({"poster_html": dynamic_html, "id": doc_id})

        else:
            return jsonify({"error": "Failed to generate poster."}), 500

    except Exception as e:
        logging.exception("An error occurred")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/updateposter/<poster_id>', methods=['POST'])
def update_poster(poster_id):
    try:
        data = request.json
        updated_html = data['poster_html']
        db.collection("posters").document(poster_id).update({"poster_html": updated_html})
        return jsonify({"message": "Poster updated successfully"})
    except Exception as e:
        logging.exception("An error occurred while updating the poster")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

@app.route('/getposters', methods=['GET'])
def get_posters():
    try:
        posters = db.collection("posters").stream()
        posters_list = [{"id": poster.id, **poster.to_dict()} for poster in posters]
        return jsonify(posters_list)
    except Exception as e:
        logging.exception("An error occurred while fetching posters")
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
