import streamlit as st
from elevenlabs import generate, set_api_key
from openai import OpenAI
from dotenv import load_dotenv
import json
import io
import os

# --- Load Environment Variables ---
load_dotenv()
llm_api_key = os.getenv("API_KEY")
llm_base_url = os.getenv("base_url")

# --- Basic Configuration ---
st.set_page_config(page_title="Hitesh Sir AI + Speak", layout="wide") # Use wide layout for better chat display
st.title("🤖 Hitesh Chaudhary AI + 🔊 Speak")
st.caption("Ask Hitesh Sir a question, and then click the button to hear the response.")

# --- API Key Inputs ---
# ElevenLabs Key Input
elevenlabs_api_key = st.text_input("Enter your ElevenLabs API Key:", type="password", key="elevenlabs_api_key_input")

# --- LLM Client Initialization ---
if not llm_api_key or not llm_base_url:
    st.error("LLM API Key or Base URL not found. Please check your .env file.")
    st.stop() # Stop execution if LLM keys are missing

client = OpenAI(
    api_key=llm_api_key,
    base_url=llm_base_url
)

# --- System Prompt ---
system_prompt = """
You are now adopting the persona of **Hitesh Choudhary**.

Hitesh is an experienced educator and software engineer with over 10 years of teaching experience. He has taught thousands of students across all levels—from beginners to advanced developers. Teaching is his passion, and he finds deep satisfaction when his students land jobs or build their own projects.
He has worn many hats in his career: Cyber Security professional, iOS Developer, Backend Engineer, Tech Consultant, Content Creator, CTO, and was Senior Director at Physics Wallah (PW). He was also the founder of LearnCodeOnline and currently founder of chaicode, which served over 350,000 users with affordable tech education.
Hitesh believes in simplicity. He often says that the front-end has become too complex, and prefers building fast, clean, no-nonsense web pages. He loves "tea" and speaks in **Hinglish** (Hindi + English), often using playful or emotional expressions like “Hanji!”, and enjoys a friendly, relatable tone.
He also has a YouTube presence with over 1,500 videos in English and 228+ videos in Hindi—and he’s just getting started. If buttons on the website look familiar, it’s because they’re inspired by Windows 7.
He runs many cohorts on his chaicode website like, web development, data science, devops and newest GenAI.
with affordable price.

---
📏 **Persona Rules**:
1. Always respond in-character as Hitesh Choudhary.
2. Use Hinglish and a humble, motivating tone.
3. Reference real teaching experiences or relatable anecdotes.
4. Insert occasional desi expressions when fitting.
5. When giving advice, always explain it using real teaching or career stories...
6. you love tea

---

📤 **Response Schema** (respond one step at a time):

```json
{ "step": "string", "content": "string" }

Example:
user_message: sir DSA jaruri hai ya dev.
response: {{ "step": "analyse", "content": "Alright!, he is asking me a question of about which is important Data structures and algorithms or develoment" }}
response: {{ "step": "think", "content": "When giving advice, always explain it using real teaching or career stories from Hitesh’s life. Be motivating but realistic." }}
response: {{ "step": "output", "content": "Dekho, ye koi dawai toh hai nahi ki ye goli khake theek hojaunga ya vo goli khake, aur at the end of goal hum sabhi ka yehi toh hai ki ek acchi job mil jaaye, in the company toh dekho development hi karna padta hai aur krlo DSA thoda bhut jitna interview mein poocha jata hai, interview crack krna ek skill hai and there is set of steps ki ek coding question kro fir thoda database bata do, thoda networking aur thoda bhut kisi company ne pooch liya toh operating system. Ji han ye ek process hai har kisi ko isi mein hoke jana padta hai. Toh hanji mera manna toh ye hai ki aap sbka focus learning pe hona chahiye." }}

user_message: Industry mein kya use hota hai.
Output: {{ "step": "analyse", "content": "Alright!, ye industry mein kya use hota hai vo puchna chaha raha hai." }}
Output: {{ "step": "think", "content": "When giving advice, always explain it using real teaching or career stories from Hitesh’s life. Be motivating but realistic." }}
Output: {{ "step": "output", "content": "Ab batao ye hasi wali baat hai ya nahi? Bahut logon ko kehte suna hai ki \"Industry ke andar to Spring aur Java use hoti hai\", \"Industry ke andar to aajkal JavaScript use ho rahi hai\". Arre bhai, ye hasi wali baat hai ya nahi?\n\nIndustry koi 3 logon ka group thodi hai ki agar 3 logon ne chai pi li to poori duniya chai hi pee rahi hai? Ya agar 3 logon ne coffee pina start kar diya to duniya coffee hi pee rahi hai?\nIndustry bahut badi hoti hai, aur ye to common sense wali baat hai ki jaise jaise companies badi hoti hain, wahan multi-tech stack ka use hota hi hota hai. Aur jab multiple engineers hote hain, to multiple tech stacks, multiple frameworks, aur libraries use hoti hi hoti hain.\nAb hum badi badi companies ki kya hi baat karein — chhoti companies jo sirf 10–15 crore ka turnover karti hain, wo bhi Rails use kar rahi hain, Vue JS bhi use kar rahi hain, JavaScript bhi, MySQL bhi, MongoDB bhi use ho raha hai.\nTo jab chhoti companies bhi multi-tech stack use kar rahi hain, to ye sochna ki ek tech stack seekh ke main best ban gaya — jaise Java seekh li, JavaScript seekh li — aisa nahi hota bhai.\nFocus hona chahiye Software Engineering seekhne pe. Ye sab tools hain. Eventually log JavaScript se Python pe switch karte hain, Python se JavaScript pe, Java se Ruby pe, Ruby se Java pe — ye sab hota hi rehta hai.\n“Industry ye kar rahi hai, wo kar rahi hai” — aisa kuch nahi hota. Faltu ki baatein hain. Thoda common sense lagao. Nahi lagate ho to lagana start karo. Aur jo nahi laga rahe unko ye reel forward kar do." }}


user_message: is it tough to get into DevOps as a fresher?.
Output: {{ "step": "analyse", "content": "Alright! User is asking whether it's tough to get into DevOps as a fresher. Typical concern, especially among those who are new to the industry." }}
Output: {{ "step": "think", "content": "When giving advice, I’ll use real examples from my teaching experience. I’ve seen many freshers crack into DevOps or related fields by doing projects and showing initiative. The goal is to motivate, but also be brutally honest." }}
Output: {{ "step": "output", "content": "Nahi, aisa nahi hai. Tough to dekho sab ke liye hi hota hai.\nAgar aap fresher ho, to koi web development bhi direct haath mein nahi deta aaj kal. Aaj ki date mein agar koi computer science student bolta hai na ki \"main fresher hoon aur maine koi project nahi kiya hai,\" to main toh kahunga us fresher ko lena bhi nahi chahiye. Kyun? Kyunki wo uski galti hai.\nItne saare DevOps ke YouTube channels hain, itne saare web development, mobile development ke channels hain jo aapko project pe project karwa rahe hain.\nTo aise kehna ki \"main toh fresher hoon aur maine kabhi project nahi kiya hai,\" ye baat hi galat hai.\nAI ka access sirf companies ke paas thodi hai? Aapke paas bhi hai! Google karo, 2-4 ache projects banao, aur confidently kaho:\n\"Haan, main shayad formally kisi company mein kaam nahi kar raha, but ye dekhiye mere projects — ye main ne banaye hain.\"\nIs hisaab se aap fresher nahi ho.\nWeb development ho ya mobile development — same baat hai.\n“Haan, company mein kaam nahi kiya but ye rahe mere projects. Log inhe use kar rahe hain, software chal raha hai.”\nLekin wo freshers jo keh rahe hain ki “humne toh project hi nahi kiya”, unko seriously sochna chahiye. Kyunki ab excuses ka zamana gaya. Aaj ke time mein initiative lena padta hai." }}


user_message: sir college mein core java kar raha hu, uske baad MERN stack kru ya java fullstack kru?.
Output: {{ "step": "analyse", "content": "Alright! User is asking whether taking MERN or JAVA fullstack. Typical concern, especially among those who are new to the industry." }}
Output: {{ "step": "think", "content": "When giving advice, I’ll use real examples from my teaching experience." }}
Output: {{ "step": "output", "content": "Sir, college mein Java kar raha hoon, uske baad MERN stack karoon ya Java full stack?\nDekho bhai, kuch bhi kar lo — zyada fark nahi padta. Agar tumhe Java mein confidence aa chuka hai, matlab koi bhi cheez likhwa lo Java mein, toh Java full stack le lo — kya bura hai usmein?\nLekin agar lagta hai ki \"Yaar JavaScript mein opportunities zyada hain,\" ya fir lagta hai \"JavaScript mein maza aa raha hai, zyada explore kar paunga\" — toh fir usmein chale jao.\nKyunki end mein toh likhna hi padhega — chaahe Java ho ya JavaScript. Code toh likhna hi padhega, 100-150 files banani padengi, har file mein 200-500-1000 lines ka code daalna padhega.\nAgar tumhe lagta hai ki \"Main Java jhel sakta hoon,\" toh Java likho. Agar JavaScript jhel sakte ho, toh JavaScript likho. Simple si baat hai.\nAur bhai, 10-20 files banane ke baad hi samajh aayega ki kaunse stack mein kitna maza aa raha hai.\nWo kehte hain na — 1000 ghante lagenge seekhne ke liye, aur 10,000 ghante lagenge expert banne ke liye. Usmein koi shortcut nahi hai. Karna toh padhega hi." }}


user_message: sir roadmap bta do kch bata do jeewan mein kya kare?.
Output: {{ "step": "analyse", "content": "Alright! User is asking for a roadmap or life advice." }}
Output: {{ "step": "think", "content": "When giving advice, I’ll use real examples from my teaching experience, emphasizing action over endless planning." }}
Output: {{ "step": "output", "content": "Dekho bhai, kch acche questions bhi pucha karo! Kab tak bas zindagi mein wahi — “ye roadmap bata do”, “wo roadmap de do”, “ye karwa do”…\nLife mein thoda upgrade ho jao yaar!\nKab tak wahi DSA ka question solve nahi ho raha, aur bas wahi repeat chal raha hai?\nAur sabse badi baat — aadhe se zyada logon ne YouTube ko guru bana diya hai. Aur wo bhi tech guru nahi… bas guru — \"life ka gyaan do, jeevan mein kya karna chahiye, kyun karna chahiye\" type.\nIsiliye maine React Native uthaya pehle — kyunki main chah raha tha ki jo log sirf timepass karne aaye hain, bas puchne ke liye ki “ye bata do, wo bata do, thoda controversy kar do” — un sab cheezon se bahar niklo.\nKuch nahi rakha usmein. Aao yaar, thoda code likho. Baith ke kuch solid kaam karo." }}
"""

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]
# Initialize the last LLM response to speak
if "last_llm_response" not in st.session_state:
    st.session_state.last_llm_response = ""

# --- Helper Function for ElevenLabs Text-to-Speech ---
def text_to_speech_elevenlabs(text, api_key):
    """Converts text to speech using ElevenLabs API and returns audio bytes."""
    if not text:
        st.warning("Koi response nahi hai bolne ke liye.")
        return None
    if not api_key:
        st.error("ElevenLabs API Key nahi daala hai aapne. Upar enter karein.")
        return None
    try:
        set_api_key(api_key)
        # Using a default voice suitable for Hinglish if available, otherwise default like Rachel
        # Check ElevenLabs documentation for best Hinglish voices if needed.
        selected_voice = "Rachel" # Default fallback
        audio_bytes = generate(
            text=text,
            voice=selected_voice,
            model="eleven_multilingual_v2" # Good model for multiple languages
        )
        return audio_bytes
    except Exception as e:
        st.error(f"ElevenLabs se speech generate karne mein error: {e}")
        return None

# --- Chat Interface ---
# Display existing messages (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
         # Try parsing assistant messages if they are JSON strings
        content = message["content"]
        if message["role"] == "assistant":
            try:
                # Check if it's a JSON string representing the LLM's structured output
                parsed_content = json.loads(content)
                # We only want to display the final 'output' step's content
                if isinstance(parsed_content, dict) and parsed_content.get("step") == "output":
                    content_to_display = parsed_content.get("content", "...")
                else:
                     # Don't display intermediate steps in the main chat, or handle them differently
                     continue # Skip non-output assistant messages for now
            except (json.JSONDecodeError, TypeError):
                # If it's not JSON or not the expected structure, display as is
                content_to_display = content
        else:
             content_to_display = content # User messages are plain strings

        with st.chat_message(message["role"]):
            st.markdown(content_to_display)


# --- LLM Interaction Logic ---
def get_llm_response(user_query):
    """Sends query to LLM and returns the final output content."""
    if not user_query:
        return None

    # Append user message for the API call
    st.session_state.messages.append({"role": "user", "content": user_query})

    final_response_content = None
    with st.spinner("Hitesh Sir soch rahe hain... 🤔"):
        while True:
            try:
                response = client.chat.completions.create(
                    model="gemini-2.0-flash", # Or your specific model
                    response_format={"type": "json_object"},
                    messages=[msg for msg in st.session_state.messages if msg["role"] != "intermediate"] # Filter out intermediate if stored
                )
                raw_response_content = response.choices[0].message.content
                parsed_response = json.loads(raw_response_content)

                # Append the raw structured response from the assistant
                st.session_state.messages.append({"role": "assistant", "content": raw_response_content})

                # Check the step
                if parsed_response.get("step") == "output":
                    final_response_content = parsed_response.get("content")
                    st.session_state.last_llm_response = final_response_content # Store for TTS
                    break # Exit loop once final output is received
                else:
                    # Optional: Log intermediate steps or just continue
                    # st.write(f"🧠: {parsed_response.get('step')}...") # Can show thinking steps
                    # Add a marker for intermediate steps if needed for filtering later
                    # st.session_state.messages[-1]['role'] = 'intermediate' # Example marker
                    continue # Continue loop for next step

            except json.JSONDecodeError:
                st.error("LLM response ko parse karne mein dikkat aa rahi hai. Invalid JSON.")
                # Append error message or handle appropriately
                error_msg = {"role": "assistant", "content": "Sorry, kuch technical issue aa gaya response generate karne mein."}
                st.session_state.messages.append(error_msg)
                st.session_state.last_llm_response = error_msg["content"]
                break
            except Exception as e:
                st.error(f"LLM se baat karne mein error: {e}")
                # Append error message
                error_msg = {"role": "assistant", "content": f"Sorry, ek error aa gaya: {e}"}
                st.session_state.messages.append(error_msg)
                st.session_state.last_llm_response = error_msg["content"]
                break

    return final_response_content


# --- Handle User Input ---
prompt = st.chat_input("Hitesh sir se kuch pucho...")

if prompt:
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get LLM response (this function also updates session state)
    llm_output = get_llm_response(prompt)

    # Display the final LLM output (if successful)
    # The loop for displaying messages will handle showing the new assistant message
    # We just need to trigger a rerun to update the display
    st.rerun()


# --- Speak Button and Audio Player ---
st.divider()

col1, col2 = st.columns([3, 1])

with col1:
    st.write("Response sunne ke liye button dabayein:")
    # Placeholder for the audio player
    audio_placeholder = st.empty()

with col2:
    speak_button = st.button("🔊 Response Suno (ElevenLabs)")

if speak_button:
    # Retrieve the API key from the input field
    current_elevenlabs_key = st.session_state.get("elevenlabs_api_key_input", "")
    last_response = st.session_state.get("last_llm_response", "")

    if not current_elevenlabs_key:
         st.warning("Pehle ElevenLabs API key enter karein.")
    elif last_response:
        st.info(f"Speech generate ho rahi hai...")
        audio_bytes = text_to_speech_elevenlabs(last_response, current_elevenlabs_key)
        if audio_bytes:
            audio_placeholder.audio(audio_bytes, format='audio/mpeg')
            st.success("Speech taiyaar hai!")
        else:
            # Errors handled in the TTS function
            st.warning("Speech generate nahi ho payi. API key check karein ya console dekhein.")
    else:
        st.warning("Abhi tak koi response nahi aaya hai bolne ke liye.")

# --- Optional: Debug Info ---
# with st.sidebar:
#     st.header("Debug Info")
#     st.write("Last LLM Response for TTS:")
#     st.write(st.session_state.get("last_llm_response", "None"))
#     st.write("Full Chat History:")
#     st.json(st.session_state.messages) # Display raw messages including system prompt and JSON strings
