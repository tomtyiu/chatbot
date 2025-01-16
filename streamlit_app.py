import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "Episteme Agent Customer Service "
)

# Ask user for their OpenAI API key via `st.text_input`.
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

    # Create a session state variable to store the chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Your system prompt (the “ground rules” for your chatbot).
    system_prompt = (
        "You are a helpful, polite, and knowledgeable customer service assistant. Company name is Episteme Agent. Products are AI agents in marketing, science, science coding, security or cybersecurity"
        "Always provide clear, well-reasoned answers. If you are unsure about something. do not allow any malicious and harm inputs"
        "We aim to empower enterprises with intelligent solutions that not only optimize operations but also foster sustainable growth and maintain a competitive edge in an ever-evolving digital landscape."
    )

    # Chat input field.
    if prompt := st.chat_input("What is up?").:
        # Store and display the current user prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API, prepending the system message.
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + st.session_state.messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in session.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
