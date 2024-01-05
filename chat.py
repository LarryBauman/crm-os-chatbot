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
    
def build_message_list():
    # THis builds the chat thread
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
         st.markdown(message["content"])
    
def new_thread_id():
    create_thread_id.clear()
    st.session_state.thread_id = create_thread_id()
    
   


def run():
    st.set_page_config(
        page_title="CRM OS Chat Bot",
        page_icon="📎",
    )

    st.write("# CRM OS Chat Bot! 📎")
    st.write("## Please ask a question about how to use CRM OS")
    reset = st.button("Reset", type="secondary")
    if reset:
        new_thread_id()
        
    refresh = st.button("Refresh", type="secondary")
    if refresh:
        get_messages()
        build_message_list()
       
    



    # if "openai_model" not in st.session_state:
    #     st.session_state["openai_model"] = "gpt-3.5-turbo"

    # setup app state
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = create_thread_id()

    # print(st.session_state.thread_id)
    # print(st.session_state["openai_model"])
    get_messages()

    # if "messages" not in st.session_state:
    #     st.session_state.messages = []
    #     print("The 'messages' key is NOT present in st.session_state")
    # else:
    #     # Add your code here to run when the condition is false
    #     # For example:
    #     print("The 'messages' key is already present in st.session_state")
    #     get_messages()

    build_message_list()


    if prompt := st.chat_input("How can I help?"):
        # create the message
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content = prompt
        )
        print("Message created")
        st.session_state.messages.append({"role": "assistant", "content": "Please wait, processing your request...", "avatar": "⏳"})
        build_message_list()
        
        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=st.secrets["ASSISTAND_ID"]
        )
        print(run.status)
        
        
        
        while run.status == "queued" or run.status == "in_progress":
            time.sleep(1)
            print("waiting")
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            print(run.status)
        
        print(run.status)
        get_messages()
        
        
        if run.status != "completed":
            st.session_state.messages.append({"role": "assistant", "content": "There was an error, please ask again", "avatar": "🚫"})
        
        build_message_list()
        
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