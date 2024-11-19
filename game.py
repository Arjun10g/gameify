import streamlit as st
import psycopg2
from psycopg2 import sql
import pandas as pd
from collections import Counter

# Function to create a connection to the database
def create_connection():
    conn = psycopg2.connect(
        host="pollmaster.postgres.database.azure.com",  # Your Azure PostgreSQL server
        database="newdb",  # Name of your database
        user="pollmaster",  # Your Azure PostgreSQL username
        password="Rocky_1995",  # Your Azure PostgreSQL password
        sslmode="require"  # Ensures secure connection
    )
    return conn

# Function to create the table if it doesn't exist
def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_responses (
            id SERIAL PRIMARY KEY,
            user_name TEXT,
            scenario TEXT,
            choice TEXT,
            outcome TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Function to insert user response into the database
def insert_response(user_name, scenario, choice, outcome):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO user_responses (user_name, scenario, choice, outcome)
        VALUES (%s, %s, %s, %s);
    """, (user_name, scenario, choice, outcome))
    conn.commit()
    cursor.close()
    conn.close()

# Function to fetch all user responses for the admin section
def fetch_all_responses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_name, scenario, choice, outcome, created_at FROM user_responses ORDER BY created_at DESC;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=["User Name", "Scenario", "Choice", "Outcome", "Timestamp"])

# Function to summarize results per user
def summarize_user_results(responses_df):
    if responses_df.empty:
        return pd.DataFrame(columns=["User Name", "Most Common Persona", "Total Responses"])

    user_persona_summary = []

    for user_name, group in responses_df.groupby("User Name"):
        most_common_persona = Counter(group["Outcome"]).most_common(1)[0][0]
        total_responses = len(group)
        user_persona_summary.append({
            "User Name": user_name,
            "Most Common Persona": most_common_persona,
            "Total Responses": total_responses
        })

    return pd.DataFrame(user_persona_summary)


# Create the table on app launch
create_table()



scenarios = [
    {
        "scenario": "The Avalanche of Data",
        "description": (
            "You’ve collected 500 hours of interviews and transcripts. Your data mountain looms large. "
            "How do you avoid being buried alive?"
        ),
        "options": [
            "Let AI blaze through it. Efficiency is king!",
            "Roll up your sleeves and tackle it manually.",
            "Team up! Let AI do the grunt work, then polish it yourself."
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Silent Speaker",
        "description": (
            "In your focus group, one participant barely speaks but their body language screams volumes. "
            "How do you make sense of their quiet contribution?"
        ),
        "options": [
            "AI can decode their few words. Minimal input, maximum output!",
            "Silence speaks louder than words. Analyze it deeply.",
            "Body language meets data analysis—combine forces!"
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "Hidden Voices",
        "description": (
            "You’re searching for marginalized perspectives hidden in a sea of data. "
            "How do you amplify these crucial voices?"
        ),
        "options": [
            "AI loves patterns—let it hunt them down!",
            "Your instincts are your compass. Trust them.",
            "Why choose? Use AI and your intuition together!"
        ],
        "outcomes": ["The Ethical Researcher", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Unexpected Insight",
        "description": (
            "AI spots a recurring theme you didn’t plan for. A goldmine or a rabbit hole? "
            "Do you follow this unexpected lead?"
        ),
        "options": [
            "Follow the AI! Let’s see where it takes us.",
            "Stay focused! Ignore the shiny distraction.",
            "Explore, but keep one foot on solid ground."
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Overwhelming Sentiment",
        "description": (
            "Your sentiment analysis tool labels everything as 'neutral.' Is your data really this boring?"
        ),
        "options": [
            "Accept it—neutral is a vibe, right?",
            "Suspicious! Question everything.",
            "Tinker with AI until it gets more interesting."
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Mysterious Outlier",
        "description": (
            "One participant’s response sticks out like a sore thumb. Outlier or hidden gem?"
        ),
        "options": [
            "Focus on the outlier—it could be groundbreaking!",
            "Ignore it—stick to the crowd.",
            "Examine both! Balance is key."
        ],
        "outcomes": ["The Ethical Researcher", "The Efficient Innovator", "The Balanced Strategist"]
    },
    {
        "scenario": "The Annotator’s Dilemma",
        "description": (
            "AI’s automated coding is, well, a bit off. How much trust do you place in your digital assistant?"
        ),
        "options": [
            "Trust AI—it’ll get better, promise!",
            "Bin AI’s suggestions. You’ve got this.",
            "Use AI’s draft and refine it yourself."
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Ethical Conundrum",
        "description": (
            "Your AI model risks exposing sensitive participant info. How do you stay ethical?"
        ),
        "options": [
            "Use AI but double down on anonymization.",
            "Ditch AI. Manual analysis for the win!",
            "Use AI selectively with strict privacy controls."
        ],
        "outcomes": ["The Ethical Researcher", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Changing Narrative",
        "description": (
            "Halfway through, AI reveals a shift in participant narratives. Pivot or stay the course?"
        ),
        "options": [
            "Go with the flow—adapt your questions.",
            "Stick to your guns. No mid-game changes.",
            "Blend both—acknowledge the shift but keep focus."
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    },
    {
        "scenario": "The Interpretation Challenge",
        "description": (
            "AI’s sentiment analysis feels a bit...off. What’s your plan?"
        ),
        "options": [
            "Trust the numbers. Data knows best!",
            "Dig deeper—manual reanalysis time.",
            "Combine AI’s stats with your qualitative genius."
        ],
        "outcomes": ["The Efficient Innovator", "The Reflexive Thinker", "The Balanced Strategist"]
    }
]

outcome_descriptions = {
    "The Ethical Researcher": "You prioritize ethics and ensure that participant confidentiality and marginalized voices are respected.",
    "The Efficient Innovator": "You harness AI's full potential to streamline processes, making research efficient without compromising quality.",
    "The Balanced Strategist": "You skillfully balance AI's capabilities with human oversight, combining speed and depth.",
    "The Reflexive Thinker": "You emphasize reflexivity, ensuring interpretations are context-sensitive and aligned with qualitative paradigms."
}


# Inject CSS for custom styling
st.markdown("""
    <style>
        .persona {
            background-color: #FAFAD2;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
            text-align: center;
            font-weight: bold;
            font-size: 1.5rem;
            color: #4B0082;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("Researcher Persona Quiz")

# Get user name
user_name = st.text_input("Enter your name:", "")

responses = []

if user_name:
    st.header("Scenarios")
    for scenario in scenarios:
        st.subheader(scenario["scenario"])
        st.write(scenario["description"])
        
        # Display options
        choice = st.radio("Choose your approach:", scenario["options"], key=scenario["scenario"])
        
        # Store user response locally
        outcome_index = scenario["options"].index(choice)
        outcome = scenario["outcomes"][outcome_index]
        responses.append((user_name, scenario["scenario"], choice, outcome))
    
    if st.button("Submit Responses"):
        for response in responses:
            insert_response(*response)
        st.success("Responses submitted successfully!")

        # Final Outcome Summary after submission
        st.header("Your Researcher Persona")
        outcomes_count = Counter([resp[3] for resp in responses])
        persona, _ = outcomes_count.most_common(1)[0]

        st.markdown(f"<div class='persona'>**You are: {persona}**<br>{outcome_descriptions[persona]}</div>", unsafe_allow_html=True)

    # Admin Section
st.header("Admin Section: All User Responses")
all_responses = fetch_all_responses()

if not all_responses.empty:
    # st.subheader("Detailed Responses")
    # st.dataframe(all_responses)

    # Summarized results for each user
    st.subheader("Overall Summary by User")
    user_summary = summarize_user_results(all_responses)

    # Display the user summary in a styled, pretty table
    st.table(user_summary)
else:
    st.warning("No responses recorded yet.")


# cd "/Users/arjunghumman/Downloads/VS Code Stuff/Python/GAMEIFY"
# streamlit run game.py