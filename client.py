from langserve import RemoteRunnable
from langchain_core.output_parsers import StrOutputParser

llm = RemoteRunnable("http://localhost:8001/basic_chat/") | StrOutputParser()
# for token in llm.stream("Hello World! How is it going?"):
#     print(token, end="")

import gradio as gr


def chat_stream(message):
    buffer = ""
    for token in llm.stream(message):
        buffer += token
        yield buffer


gr.ChatInterface(chat_stream).queue().launch(share=False, debug=True)


# ######################################################
# # Non-streaming Interface like that shown above


# def rhyme_chat(message, history):
#     return llm.invoke(message)


# gr.ChatInterface(rhyme_chat).launch()

# ######################################################
