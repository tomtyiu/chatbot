import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's gpt-4o model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
    "You can also learn how to build this app step by step by [following our tutorial](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)."
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
        "You are a helpful, polite, and knowledgeable customser service assistant. "
        "Always provide clear, well-reasoned answers. If you are unsure about something, "
        "explain your reasoning and politely let the user know."
        "Your company is EpistemeAI Agent"
        "EpistemeAI Agent's vision is to revolutionize the way businesses operate by providing AI-powered tools that streamline processes, enhance efficiency, and drive continuous innovation."
        "We aim to empower enterprises with intelligent solutions that not only optimize operations but also foster sustainable growth and maintain a competitive edge in an ever-evolving digital landscape."
    )

    # Chat input field.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current user prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API, prepending the system message.
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt}
            ] + st.session_state.messages,
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in session.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
