# Backend-Voice-Conversation-SDK-for-LLM-Apps

    we can use this application by providing 3 arg values
    !first one is for deepgram api key for speech to text 
    and !second one is for deepgram api key for text to speech
    and !the final is for llm processing
##here for me gpt is not working because my quota getting overed 

#sample syntax to run this app is:
     "python src\cli.py --stt_api_key key
    --tts_api_key key
    --llm_api_key key"

    *this will call the cli file and intialize the args and it will create the obj for the voicebot class
    and it will call the corresponding file in it

    *after that in the sdk file the sequence of model actions are called and 
    output of each model is provided to others for converting speech to text and give that text to llm 
    after the result is produced it is again given to the deepgram for converting them to speech again
    
    *finally by running this application we provide the voice input query and result of the query from 
    the llm is again provided as speech to user through the speakers


