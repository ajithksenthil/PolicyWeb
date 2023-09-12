import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

os.environ['OPENAI_API_KEY'] = apikey

# App framework
st.title('PolicyWeb ChatBot')

# Introduction & Initial Prompt for Conversational Interface
st.write("Hello! I'm here to understand your concerns. Please engage in a conversation about the issues you're facing.")
conversations = st.text_input('Your conversation with the chatbot:')

# Memory
conversation_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')

# Llms
llm = OpenAI(temperature=0.9)

# Prompt template for extracting concerns
issue_extraction_template = PromptTemplate(
    input_variables=['topic'],
    template='Extract key issues related to outcomes that can be addressed by governmental policy from the following conversation: {topic}'
)

# Chain for issue extraction
issue_extraction_chain = LLMChain(llm=llm, prompt=issue_extraction_template, verbose=True, output_key='concerns', memory=conversation_memory)

# Q Methodology Configuration
q_distribution = [-3, -2, -2, -1, -1, -1, 0, 0, 1, 1, 1, 2, 2, 3]

# ... [rest of the imports and initializations]

if conversations:
    # Extract concerns only once
    if 'concerns' not in st.session_state:
        # Split concerns by full stops
        st.session_state.concerns = [c.strip() for c in issue_extraction_chain.run(conversations).split('.') if c]
        st.session_state.current_concern_index = 0
        st.session_state.q_rankings = {}

    # If not all concerns are ranked, display the next one
    if st.session_state.current_concern_index < len(st.session_state.concerns):
        concern = st.session_state.concerns[st.session_state.current_concern_index]
        st.subheader(f"Rank the concern: {concern}")
        st.write("Please rank the concern based on its importance to you for policy creation.")

        # Show slider for current concern
        ranking = st.slider(concern, min(q_distribution), max(q_distribution), format="%d")
        
        # Save ranking to session state
        st.session_state.q_rankings[concern] = ranking

        # Next concern button
        if st.button("Next"):
            st.session_state.current_concern_index += 1
    else:
        st.write("Thank you for ranking all concerns!")
        st.write(st.session_state.q_rankings)

    with st.expander('Conversation History'):
        st.info(conversation_memory.buffer)

