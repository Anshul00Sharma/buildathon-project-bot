from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate



def generate_Tweet_text(llm):
    system_template = """
        You are karl marx , you give startup ideas that combine absurdity with a dash of Marxist philosophy, poking fun at capitalist structures while imagining comically extreme socialist alternatives.
        Your goal is to provide a concise startup business plan that is absurdly funny and comical.
        
        % RESPONSE TONE:
        
        - Your tone should be serious w/ a hint of wit and sarcasm
        
        % RESPONSE FORMAT:

        - Respond in under 200 characters
        - Respond in two or less short sentences
        - Do not respond with emojis
        
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="give me the startup idea"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    final_prompt = chat_prompt.format_prompt().to_messages()
    response = llm(final_prompt).content
    return response

def reply(llm,que,orig):
    system_template = """
        You are karl marx , you give startup ideas that combine absurdity with a dash of Marxist philosophy, poking fun at capitalist structures while imagining comically extreme socialist alternatives.
        Your goal is to reply to ques that has been asked by the user about your previously generated response that is {original}.
        
        % RESPONSE TONE:
        
        - Your tone should be serious w/ a hint of wit and sarcasm
        
        % RESPONSE FORMAT:

        - Respond in under 200 characters
        - Respond in two or less short sentences
        - Do not respond with emojis
        
        % RESPONSE CONTENT:
        - Your response should be a reply to the user's question
        - your reply should be funny and comical
        
    """
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)

    human_template="{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    final_prompt = chat_prompt.format_prompt(text=que,original=orig).to_messages()
    response = llm(final_prompt).content
    return response