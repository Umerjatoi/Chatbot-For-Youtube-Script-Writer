import streamlit as st 
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import DuckDuckGoSearchRun

# Applying Styling
st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#FFFFFF;
    }
</style>""", unsafe_allow_html=True)


# Creating Session State Variable
if 'API_Key' not in st.session_state:
    st.session_state['API_Key'] =''


st.title('❤️ YouTube Script Writing Tool💗') 
# st.header("YOUTUBE SCRIPT TOOL WITH OPENAI ")

# Sidebar to capture the OpenAi API key
st.sidebar.title("😎🗝️")
st.session_state['API_Key']= st.sidebar.text_input("What's your API key?",type="password")
st.sidebar.image('./Youtube.jpg',width=300, use_column_width=True)


# Captures User Inputs
prompt = st.text_input('Please provide the topic of the video',key="prompt")  # The box for the text prompt
video_length = st.text_input('Expected Video Length 🕒 (in minutes)',key="video_length")  # The box for the text prompt
creativity = st.slider('Words limit ✨ - (0 LOW || 1 HIGH)', 0.0, 1.0, 0.2,step=0.1)
submit = st.button("Generate Script for me")
# Function to generate video script
def generate_script(prompt,video_length,creativity,api_key):
    
    # Template for generating 'Title'
    title_template = PromptTemplate(
        input_variables = ['subject'], 
        template='Please come up with a title for a YouTube video on the  {subject}.'
        )

    # Template for generating 'Video Script' using search engine
    script_template = PromptTemplate(
        input_variables = ['title', 'DuckDuckGo_Search','duration'], 
        template='Create a script for a YouTube video based on this title for me. TITLE: {title} of duration: {duration} minutes using this search data {DuckDuckGo_Search} '
    )

    #Setting up OpenAI LLM
    llm = OpenAI(temperature=creativity,openai_api_key=api_key,
            model_name='text-davinci-003') 
    
    #Creating chain for 'Title' & 'Video Script'
    title_chain = LLMChain(llm=llm, prompt=title_template, verbose=True)
    script_chain = LLMChain(llm=llm, prompt=script_template, verbose=True)

    
    # https://python.langchain.com/docs/modules/agents/tools/integrations/ddg
    search = DuckDuckGoSearchRun()

    # Executing the chains we created for 'Title'
    title = title_chain.run(prompt)

    # Executing the chains we created for 'Video Script' by taking help of search engine 'DuckDuckGo'
    search_result = search.run(prompt) 
    script = script_chain.run(title=title, DuckDuckGo_Search=search_result,duration=video_length)

    # Returning the output
    return search_result,title,script
  
if submit:
    
    if st.session_state['API_Key']:
        search_result,title,script = generate_script(prompt,video_length,creativity,st.session_state['API_Key'])
        #Let's generate the script
        st.success('Hope you like this script ❤️')

        #Display Title
        st.subheader("Title:🔥")
        st.write(title)

        #Display Video Script
        st.subheader("Your Video Script:📝")
        st.write(script)

        #Display Search Engine Result
        st.subheader("Check Out - DuckDuckGo Search:🔍")
        with st.expander('Show me 👀'): 
            st.info(search_result)
    else:
        st.error("Ooopssss!!! Please provide API key.....")
