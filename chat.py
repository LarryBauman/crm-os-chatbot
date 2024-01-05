import streamlit as st
import time
from streamlit.logger import get_logger

from openai import OpenAI

LOGGER = get_logger(__name__)
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

@st.cache_data
def create_thread_id():
    thread = client.beta.threads.create()
    # print(thread.id)
    return thread.id
    # return "thread_YzxFRCTtWA7dl0aQRdlvaOCy"

def get_messages():
    messages = client.beta.threads.messages.list(thread_id=st.session_state.thread_id)
    
    sorted_messages = sorted(messages.data, key=lambda m: m.created_at, reverse=False)
    
    st.session_state.messages = [
        {"role": m.role, "content": m.content[0].text.value, "avatar": "🤷" if m.role == "user" else "📎"} for m in sorted_messages
    ]
   


def run():
    st.set_page_config(
        page_title="CRM OS Chat Bot",
        page_icon="📎",
    )

    st.write("# CRM OS Chat Bot! 📎")
    st.write("## Please ask a question about how to use CRM OS")



    # if "openai_model" not in st.session_state:
    #     st.session_state["openai_model"] = "gpt-3.5-turbo"

    # setup app state
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = create_thread_id()

    # print(st.session_state.thread_id)
    # print(st.session_state["openai_model"])


    if "messages" not in st.session_state:
        st.session_state.messages = []
    else:
        # Add your code here to run when the condition is false
        # For example:
        print("The 'messages' key is already present in st.session_state")
        get_messages()

    # THis builds the chat thread
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
         st.markdown(message["content"])

    if prompt := st.chat_input("How can I help?"):
        # create the message
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content = prompt
        )
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=st.secrets["ASSISTAND_ID"]
        )
        print(run.status)
        
        st.session_state.messages.append({"role": "assistant", "content": "Please wait, processing your request..."})
        
        while run.status == "queued":
            time.sleep(1)
            print("waiting")
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
        get_messages()
        
        
        
        # st.session_state.messages.append({"role": "user", "content": prompt})
        # with st.chat_message("user"):
        #     st.markdown(prompt)

        # with st.chat_message("assistant"):
        #     message_placeholder = st.empty()
        #     full_response = "This is just  a test"
        #     # for response in client.chat.completions.create(
        #     #     model=st.session_state["openai_model"],
        #     #     messages=[
        #     #         {"role": m["role"], "content": m["content"]}
        #     #         for m in st.session_state.messages
        #     #     ],
        #     #     stream=True,
        #     # ):
        #     #     full_response += (response.choices[0].delta.content or "")
        #     #     message_placeholder.markdown(full_response + "▌")
        #     message_placeholder.markdown(full_response)
        # st.session_state.messages.append({"role": "assistant", "content": full_response})




if __name__ == "__main__":
    run()