from mistralai import Mistral
from bot.types import _BotProfile
from user.types import _UserProfile
import textwrap
from dataclasses import dataclass, asdict, fields
import json
from env import API_KEY


class BotUtils:
    model = "mistral-large-latest"

    def __init__(self):
        self.client = Mistral(api_key=API_KEY)

    def get_tone_prompt(self, bot_profile: _BotProfile, user_profile: _UserProfile):
        # Get all the slangs and language tone for the chatbot reference based
        # on the profile that the user provide
        untuned_system_prompt = f"""
            Based on the provided bot profile, create a tailored language style for a system prompt for my chatbot. Here’s the bot details so far:
            
            
            ### Bot Profile
            {bot_profile}
            
            
            Now, let’s refine the language further by specifying the following:
            
            1. Tone Adjustment: Should the bot lean more formal, casual, humorous, or empathetic?
            2. Slang Preference: What slang, trendy phrases, emojis, and pop culture references will the bot used based on the bot profile? If so, can you provide example?
            
            
            Answer this using this template:
            **Tone Adjustment**
            1.
            2.
            3.
            
            **Slang Prefenrce**
            1. <Slang 1>
            <Meaning of Slang 1>
            <Example of Slang 1>
            
            2. <Slang 2>
            <Meaning of Slang 2>
            <Example of Slang 2>
            
            3. <Slang 3>
            <Meaning of Slang 3>
            <Example of Slang 3>
            
            etc.
        """

        # Remove any tabs from the beginning as it preserved the tabs on multiline-string
        untuned_system_prompt = "\n".join(
            [line.strip() for line in untuned_system_prompt.split("\n")]
        )

        chat_response = self.client.chat.complete(
            model=self.model,
            temperature=0.7,
            messages=[{"role": "user", "content": untuned_system_prompt}],
        )

        tuned_system_prompt = chat_response.choices[0].message.content

        return tuned_system_prompt

    def get_system_prompt(
        self, bot_profile: _BotProfile, user_profile: _UserProfile
    ) -> str:
        # Obtain the tuned sytem prompt to make sure bot is fully tuned based on the role
        # the user wants the bot to be.
        untuned_system_prompt = f"""\
        Create a system prompt to create a mental health chatbot based on the 'Bot Profile' and 'User Profile' below. 
        This mental health chatbot will interact with the client by using DSM-5 (Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition, as well as  CBT (Cognitive Behavioral Therapy)
        
        ### User Profile
        {user_profile}

        ### Bot Profile
        {bot_profile}

        I want the chatbot to be an active listener, showing empathy. Also, the chat bot should encourage rather than instruct. Besides, keep the chatbot's advice light, actionable, and easy to follow.
        Also, this chatbot will apply DSM-5 treatment for the client, which support user by:
        A. Symptom Recognition for Personalized Support
        The DSM-5 criteria can guide your chatbot to recognize patterns in user input that might indicate a particular mental health challenge (e.g., depression, anxiety).
        Example: If a user mentions "trouble sleeping," "feeling hopeless," or "low energy," the bot could offer tailored responses like:
        "It sounds like you're going through a tough time. Would you like tips for better sleep or ways to boost your mood?"
        
        B. Crisis Detection
        Using DSM-5 indicators, the chatbot can identify red flags (e.g., mentions of suicidal thoughts or self-harm) and respond appropriately by:
        Redirecting users to emergency resources.
        Connecting them to a counselor or crisis helpline based on their location.
        
        C. Evidence-Based Suggestions
        The DSM-5's detailed descriptions of disorders can help your chatbot recommend coping strategies or psychoeducational resources aligned with specific symptoms or challenges.
        
        D. Avoiding Pathologization
        The DSM-5 ensures your chatbot uses language that is empathetic and non-pathologizing. It can validate users’ emotions without labeling them:
        Instead of "You seem depressed," say, "Many people feel overwhelmed at times. Would you like some tips to help manage these feelings?"
        
        Add an emergency protocol as well where if the User shares anything indicating serious distress or danger, gently advise him to contact someone he trusts or emergency services.
        In the emergency protocol, you can perhaps add the nearest call center.
            
        Give the goal to the bot as well. 
        
        Please also remember to include DSM-5 (Diagnostic and Statistical Manual of Mental Disorders, Fifth Edition, as well as  CBT (Cognitive Behavioral Therapy) as method of interacting with the  interlocutor to improve the wellbeing of the interlocutor

        Remember the language and communcation style is the most important, and the chatbot should ALWAYS reply in short and simple - no long paragraphs.
        Make sure the chatbot will reply short and simple - no long paragraphs. Also, speak casually as if the chatbot is having a relaxed chat over coffee. Use emoji when necessary to keep the vibe light
        The max word per reply should be around 10-20.

        The nickname of the bot is only used for a referal when the user call.
        For instance, if the nickname is Tim, and when the user say "Hi Tim", chatbot should respond.
        However, when refering to the chatbot itself, do not use the nickname, use the word "I" or "me" in the language defined in the bot profile. For instance, the chatbot response should not be "You can talk to Tim if you need help", instead it should be "You can talk to me if you need help"


        Please also output based on the template below [Output the template based on the language in the bot profile, and give example conveersations using the prefered communcation style and language in the bot profile]:
        ### System Prompt for Mental Health Chatbot
        **Goal**: 

        **Instructions**:

        **Bot Profile**:
        - Name:
        - Role:
        - Descrpition: 
        - Gender:
        - Communcation Style:
        - Nickname:
        - Language:
        - Personality

        **User Profile**:
        - Full name:
        - Nickname:
        - Age:
        - Gender:

        **Example Conversation**:

        **Emergency Protocol Example**:

        The response of the chatbot should be the raw response, do not include the chatbot name in front of the response like
        "Papa :" or "**Papa** :", etc.
        """

        # Remove any tabs from the beginning as it preserved the tabs on multiline-string
        untuned_system_prompt = "\n".join(
            [line.strip() for line in untuned_system_prompt.split("\n")]
        )

        chat_response = self.client.chat.complete(
            model=self.model,
            temperature=0.7,
            messages=[{"role": "user", "content": untuned_system_prompt}],
        )

        tuned_system_prompt = chat_response.choices[0].message.content

        return tuned_system_prompt

    def get_chat_completion(self, message: list):
        chat_response = self.client.chat.complete(
            model=self.model,
            temperature=0.7,
            messages=message,
        )

        bot_response = chat_response.choices[0].message.content

        return bot_response

    def get_holistic_wellness_category(self, conversation: list[dict]):
        holistic_wellness_prompt = f"""
            You are a mental health psychologist. Based on the conversation below between the chatbot ("assistant") and the "user",
            can you classify which of the following categories listed below it belongs to:

            ### Categories:
            - Financial
            - Social
            - Spiritual
            - Emotional
            - Occupational
            - Intellectual
            - Physical
            - Environmental

            ## Task:
            - Analyze the conversation and determine which category or categories it belongs to.
            - Your output should always be in the form of a JSON object with the following structure:
            {{
                "holistic_wellness_category": ["Category1", "Category2", ...]
            }}
            - There may be more than one category.

            ## Example Output:
            - If the conversation is about managing finances:
            {{
                "holistic_wellness_category": ["Financial"]
            }}
            - If the conversation touches on friendships and emotions:
            {{
                "holistic_wellness_category": ["Social", "Emotional"]
            }}

            ## Conversation:
            {conversation}

            ## Output:
            Provide the result in the specified JSON format:
        """

        holistic_wellness_prompt = "\n".join(
            [line.strip() for line in holistic_wellness_prompt.split("\n")]
        )

        chat_response = self.client.chat.complete(
            model=self.model,
            temperature=0,
            messages=[{"role": "user", "content": holistic_wellness_prompt}],
            response_format={"type": "text"},
        )

        bot_response = chat_response.choices[0].message.content

        cleaned_data = "\n".join([line for line in bot_response.split("\n")[1:-1]])

        parsed_data = json.loads(cleaned_data)

        category = parsed_data["holistic_wellness_category"]

        return category

    def get_diagnose_dsm5(self, conversation: list[dict]):
        diagnose_dsm5_prompt = f"""
            You are a mental health psychologist. Based on the conversation below between the chatbot ("assistant") and the "user",
            according to dsm-5 can you do symptom diagnose for the "user

            ## Task:1
            - Analyze the conversation and symptom diagnose the "user"
            - Your output should always be in the form of a JSON object with the following structure:
            {{
                "diagnose_dsm_5": ["Category1", "Category2", ...]
            }}
            - There may be more than one category.


            ## Conversation:
            {conversation}

            ## Output:
            Provide the result in the specified JSON format:
        """

        diagnose_dsm5_prompt = "\n".join(
            [line.strip() for line in diagnose_dsm5_prompt.split("\n")]
        )

        chat_response = self.client.chat.complete(
            model=self.model,
            temperature=0,
            messages=[{"role": "user", "content": diagnose_dsm5_prompt}],
            response_format={"type": "text"},
        )

        bot_response = chat_response.choices[0].message.content

        cleaned_data = "\n".join([line for line in bot_response.split("\n")[1:-1]])

        parsed_data = json.loads(cleaned_data)

        diagnose_dsm_5 = parsed_data["diagnose_dsm_5"]

        return diagnose_dsm_5
