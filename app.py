import streamlit as st
import boto3
import json
from app.utils.prompt import get_patient_prompt, get_feedback_prompt
from app.config import AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_SESSION_TOKEN, AWS_DEFAULT_REGION

# Initialize AWS Bedrock Agent Runtime client
client = boto3.client(
    'bedrock-agent-runtime',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    aws_session_token=AWS_SESSION_TOKEN,
    region_name=AWS_DEFAULT_REGION
)

# Set page configuration (wide layout for better appearance)
st.set_page_config(page_title="Flamingo Cares - Patient Simulator", layout="wide")

# Inject custom CSS for improved UI
st.markdown(
    """
    <style>
    /* Center the title */
    .centered-title {
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        color: #2E86C1;
        margin-bottom: 20px;
    }
    /* Chat container with scrollable area */
    .chat-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background-color: #f7f7f7;
        border: 1px solid #ddd;
        border-radius: 10px;
        margin: 0 auto;
        max-width: 800px;
        width: 100%;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Chat bubbles */
    .chat-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        max-width: 70%;
        margin: 8px 0;
        word-wrap: break-word;
        font-size: 16px;
        line-height: 1.5;
    }
    .chat-bubble.user {
        background-color: #2E86C1;  /* Blue for user messages */
        color: white;
        align-self: flex-end;
        margin-left: auto;
    }
    .chat-bubble.bot, .chat-bubble.System {
        background-color: #ffffff;  /* White for bot/system messages */
        align-self: flex-start;
        margin-right: auto;
        border: 1px solid #ddd;
    }
    /* Fixed input area at the bottom */
    .input-area {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #ffffff;
        border-top: 1px solid #ddd;
        padding: 16px 20px;
        display: flex;
        justify-content: center;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
    }
    .input-area .stTextInput {
        width: 600px;
        max-width: 100%;
        margin-right: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    .input-area .stButton button {
        background-color: #2E86C1;  /* Blue for the send button */
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
    }
    .input-area .stButton button:hover {
        background-color: #2471A3;  /* Darker blue on hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered title
st.markdown("<h1 class='centered-title'>Flamingo Cares - Patient Simulator</h1>", unsafe_allow_html=True)

# Sidebar for instructions on how to use the app
with st.sidebar:
    st.header("How to Use This App")
    st.markdown("""
    **Flamingo Cares - Patient Simulator** is a virtual patient system designed for training medical professionals. Here's how to interact with the app:

    1. **Type your message**: Enter questions or instructions as a doctor and send them to the patient. 
    2. **Patient's Response**: The app simulates a patient's response based on your input. 
    3. **End Conversation**: Type "END" to end the conversation, and the patient will provide feedback on your anamnesis.
    4. **Feedback**: Once the conversation ends, you'll receive feedback on your interactions with the patient.

    The app utilizes **AWS Bedrock Agent** for intelligent responses and medical training purposes.

    _Use this app to practice your diagnostic skills, improve patient communication, and enhance your medical training._
    """)

# Initialize chat history in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Create a container for the entire chat interface
chat_wrapper = st.container()

# Placeholder for chat messages (so we can update it)
chat_placeholder = st.empty()

def render_chat():
    chat_html = "<div class='chat-container'>"
    for role, text in st.session_state.chat_history:
        # Use 'System' messages as a separate CSS class if needed
        css_class = "user" if role == "Doctor" else "bot"
        chat_html += f"<div class='chat-bubble {css_class}'><strong>{role}:</strong> {text}</div>"
    chat_html += "</div>"
    chat_placeholder.markdown(chat_html, unsafe_allow_html=True)

# Render the chat history
render_chat()

# Fixed input area (using a form to clear input after submission)
st.markdown("<div class='input-area'>", unsafe_allow_html=True)
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("Message", placeholder="Type your message here...", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("Send")
st.markdown("</div>", unsafe_allow_html=True)

# Process the input after submission
if submitted and user_input:
    # Append the user's message
    st.session_state.chat_history.append(("Doctor", user_input))
    render_chat()

    # If the conversation is ending, provide feedback; otherwise, simulate patient response.
    if user_input.lower() == "end":
        st.session_state.chat_history.append(("System", "END of the conversation. The patient will now provide feedback on your anamnesis."))
        render_chat()
        try:
            response = client.retrieve_and_generate(
                input={'text': get_feedback_prompt(user_input)},
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'modelArn': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
                        'knowledgeBaseId': 'WDN1MVE1HZ',
                        'generationConfiguration': {
                            'inferenceConfig': {
                                'textInferenceConfig': {
                                    'maxTokens': 1500,
                                    'temperature': 0.3,
                                    'topP': 0.9
                                }
                            }
                        },
                        'retrievalConfiguration': {
                            'vectorSearchConfiguration': {
                                'numberOfResults': 5
                            }
                        }
                    }
                }
            )
            if 'output' in response and 'text' in response['output']:
                feedback_response = response['output']['text']
                st.session_state.chat_history.append(("Patient Feedback", feedback_response))
            else:
                st.session_state.chat_history.append(("System", "Error: No response text found in the output."))
        except Exception as e:
            st.session_state.chat_history.append(("System", f"An error occurred: {e}"))
    else:
        try:
            response = client.retrieve_and_generate(
                input={'text': get_patient_prompt(user_input)},
                retrieveAndGenerateConfiguration={
                    'type': 'KNOWLEDGE_BASE',
                    'knowledgeBaseConfiguration': {
                        'modelArn': 'anthropic.claude-3-5-sonnet-20241022-v2:0',
                        'knowledgeBaseId': 'WDN1MVE1HZ',
                        'generationConfiguration': {
                            'inferenceConfig': {
                                'textInferenceConfig': {
                                    'maxTokens': 1500,
                                    'temperature': 0.3,
                                    'topP': 0.9
                                }
                            }
                        },
                        'retrievalConfiguration': {
                            'vectorSearchConfiguration': {
                                'numberOfResults': 5
                            }
                        }
                    }
                }
            )
            if 'output' in response and 'text' in response['output']:
                patient_response = response['output']['text']
                st.session_state.chat_history.append(("Patient", patient_response))
            else:
                st.session_state.chat_history.append(("System", "Error: No response text found in the output."))
        except Exception as e:
            st.session_state.chat_history.append(("System", f"An error occurred: {e}"))
    render_chat()

