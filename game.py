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
            "Use AI to summarize key points quickly and efficiently.",  # Efficient Innovator
            "Manually work through the data to ensure depth and accuracy.",  # Reflexive Thinker
            "Let AI handle the initial organization, then refine it personally."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "The Silent Speaker",
        "description": (
            "In your focus group, one participant barely speaks, but their body language speaks volumes. "
            "How do you make sense of their quiet contribution?"
        ),
        "options": [
            "Use AI tools to analyze their few words and non-verbal cues.",  # Efficient Innovator
            "Deeply reflect on their silence and interpret it qualitatively.",  # Reflexive Thinker
            "Combine AI sentiment analysis with your observations."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "Hidden Voices",
        "description": (
            "You’re searching for marginalized perspectives hidden in a sea of data. "
            "How do you amplify these crucial voices?"
        ),
        "options": [
            "Let AI scan for recurring patterns and amplify these voices.",  # Efficient Innovator
            "Trust your qualitative instincts to uncover marginalized perspectives.",  # Reflexive Thinker
            "Blend AI’s insights with your interpretations to ensure no voice is missed."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "The Unexpected Insight",
        "description": (
            "AI spots a recurring theme you didn’t plan for. A goldmine or a rabbit hole? "
            "Do you follow this unexpected lead?"
        ),
        "options": [
            "Let AI guide you to explore this new theme efficiently.",  # Efficient Innovator
            "Ignore it and stay focused on your original research plan.",  # Reflexive Thinker
            "Explore the theme cautiously while keeping your primary goals in sight."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "The Overwhelming Sentiment",
        "description": (
            "Your sentiment analysis tool labels everything as 'neutral.' Is your data really this boring?"
        ),
        "options": [
            "Accept the results—neutrality is valid too!",  # Efficient Innovator
            "Question the analysis and reanalyze the data manually.",  # Reflexive Thinker
            "Tweak the AI model to better detect subtle emotional patterns."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "The Annotator’s Dilemma",
        "description": (
            "AI’s automated coding is, well, a bit off. How much trust do you place in your digital assistant?"
        ),
        "options": [
            "Trust AI—it’s efficient and will improve over time.",  # Efficient Innovator
            "Discard AI’s coding and rely solely on your expertise.",  # Reflexive Thinker
            "Use AI’s coding as a draft and refine it yourself."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "The Ethical Conundrum",
        "description": (
            "Your AI model risks exposing sensitive participant info. How do you stay ethical?"
        ),
        "options": [
            "Use anonymization techniques to protect participants.",  # Efficient Innovator
            "Avoid AI altogether and stick to manual analysis.",  # Reflexive Thinker
            "Implement strict privacy controls to safely use AI."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    },
    {
        "scenario": "The Changing Narrative",
        "description": (
            "Halfway through, AI reveals a shift in participant narratives. Pivot or stay the course?"
        ),
        "options": [
            "Go with the flow—adapt your questions.",  # Efficient Innovator
            "Stick to your guns. No mid-game changes.",  # Reflexive Thinker
            "Blend both—acknowledge the shift but keep focus."  # Balanced Strategist
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist"
        ]
    }
]

outcome_descriptions = {
    "The Efficient Innovator": "You fully leverage AI's potential to streamline processes, driving efficiency while maintaining high research quality.",
    "The Reflexive Thinker": "You prioritize reflexivity, ensuring your research interpretations remain context-sensitive and grounded in qualitative traditions.",
    "The Balanced Strategist": "You skillfully balance AI's capabilities with human intuition, merging speed with thoughtful depth in your research."
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
st.title("Data Feud: The Researcher’s Dilemma")

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
# Admin Section with Password Protection
st.header("Admin Section")

def check_admin_access():
    admin_password = "qualitative"  # Set your secure admin password here
    entered_password = st.text_input("Enter admin password:", type="password")
    
    if st.button("Submit Password"):
        if entered_password == admin_password:
            st.success("Access granted!")
            return True
        else:
            st.error("Incorrect password. Please try again.")
            return False
    return False

if check_admin_access():
    all_responses = fetch_all_responses()

    if not all_responses.empty:
        # Summarized results for each user
        st.subheader("Overall Summary by User")
        user_summary = summarize_user_results(all_responses)

        # Display the user summary in a styled, pretty table
        st.table(user_summary)
    else:
        st.warning("No responses recorded yet.")
else:
    st.warning("Enter the correct admin password to view this section.")

# cd "/Users/arjunghumman/Downloads/VS Code Stuff/Python/GAMEIFY"
# streamlit run game.py