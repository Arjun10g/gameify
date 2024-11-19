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
            "Let AI blaze through it. Efficiency is king!",  # Efficient Innovator
            "Roll up your sleeves and tackle it manually.",  # Reflexive Thinker
            "Team up! Let AI do the grunt work, then polish it yourself.",  # Balanced Strategist
            "Find hidden gems in outlier data using advanced AI models.",  # Data Explorer
            "Focus on data security and ethics while processing it.",  # Ethical Researcher
            "Carefully evaluate risks before using AI on sensitive datasets."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "The Silent Speaker",
        "description": (
            "In your focus group, one participant barely speaks but their body language screams volumes. "
            "How do you make sense of their quiet contribution?"
        ),
        "options": [
            "AI can decode their few words. Minimal input, maximum output!",  # Efficient Innovator
            "Silence speaks louder than words. Analyze it deeply.",  # Reflexive Thinker
            "Combine AI’s sentiment analysis with your intuition.",  # Balanced Strategist
            "Explore body language data for hidden narratives.",  # Data Explorer
            "Prioritize ethics—ensure they aren’t misrepresented.",  # Ethical Researcher
            "Proceed cautiously, ensuring data privacy.",  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "Hidden Voices",
        "description": (
            "You’re searching for marginalized perspectives hidden in a sea of data. "
            "How do you amplify these crucial voices?"
        ),
        "options": [
            "AI loves patterns—let it hunt them down!",  # Efficient Innovator
            "Your instincts are your compass. Trust them.",  # Reflexive Thinker
            "Why choose? Use AI and your intuition together!",  # Balanced Strategist
            "Dig deep for unheard voices and unexpected stories.",  # Data Explorer
            "Ensure marginalized voices are represented ethically.",  # Ethical Researcher
            "Be cautious about potential biases in AI models."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "The Unexpected Insight",
        "description": (
            "AI spots a recurring theme you didn’t plan for. A goldmine or a rabbit hole? "
            "Do you follow this unexpected lead?"
        ),
        "options": [
            "Follow the AI! Let’s see where it takes us.",  # Efficient Innovator
            "Stay focused! Ignore the shiny distraction.",  # Reflexive Thinker
            "Explore, but keep one foot on solid ground.",  # Balanced Strategist
            "Unearth new patterns and dive into the unknown.",  # Data Explorer
            "Ensure the new direction aligns with ethical guidelines.",  # Ethical Researcher
            "Assess risks before venturing into new territory."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "The Overwhelming Sentiment",
        "description": (
            "Your sentiment analysis tool labels everything as 'neutral.' Is your data really this boring?"
        ),
        "options": [
            "Accept it—neutral is a vibe, right?",  # Efficient Innovator
            "Suspicious! Question everything.",  # Reflexive Thinker
            "Adjust AI models to better capture nuance.",  # Balanced Strategist
            "Dig deeper to find subtle emotional patterns.",  # Data Explorer
            "Ensure neutral labeling doesn't mask important perspectives.",  # Ethical Researcher
            "Evaluate potential biases and fix the analysis model."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "The Mysterious Outlier",
        "description": (
            "One participant’s response sticks out like a sore thumb. Outlier or hidden gem?"
        ),
        "options": [
            "Focus on the outlier—it could be groundbreaking!",  # Data Explorer
            "Ignore it—stick to the crowd.",  # Efficient Innovator
            "Examine both! Balance is key.",  # Balanced Strategist
            "Analyze deeply for ethical implications.",  # Ethical Researcher
            "Investigate, but tread cautiously.",  # Risk-Conscious Analyst
            "Think deeply about why it stands out.",  # Reflexive Thinker
        ],
        "outcomes": [
            "The Data Explorer",
            "The Efficient Innovator",
            "The Balanced Strategist",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst",
            "The Reflexive Thinker"
        ]
    },
    {
        "scenario": "The Annotator’s Dilemma",
        "description": (
            "AI’s automated coding is, well, a bit off. How much trust do you place in your digital assistant?"
        ),
        "options": [
            "Trust AI—it’ll get better, promise!",  # Efficient Innovator
            "Bin AI’s suggestions. You’ve got this.",  # Reflexive Thinker
            "Use AI’s draft and refine it yourself.",  # Balanced Strategist
            "Explore to discover unintended patterns.",  # Data Explorer
            "Ensure the coding aligns with ethical research standards.",  # Ethical Researcher
            "Evaluate risks before fully trusting AI suggestions."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "The Ethical Conundrum",
        "description": (
            "Your AI model risks exposing sensitive participant info. How do you stay ethical?"
        ),
        "options": [
            "Use AI but double down on anonymization.",  # Ethical Researcher
            "Ditch AI. Manual analysis for the win!",  # Reflexive Thinker
            "Use AI selectively with strict privacy controls.",  # Balanced Strategist
            "Analyze the risks thoroughly before proceeding.",  # Risk-Conscious Analyst
            "Uncover insights without compromising safety.",  # Data Explorer
            "Maximize efficiency while adhering to privacy standards."  # Efficient Innovator
        ],
        "outcomes": [
            "The Ethical Researcher",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Risk-Conscious Analyst",
            "The Data Explorer",
            "The Efficient Innovator"
        ]
    },
    {
        "scenario": "The Changing Narrative",
        "description": (
            "Halfway through, AI reveals a shift in participant narratives. Pivot or stay the course?"
        ),
        "options": [
            "Go with the flow—adapt your questions.",  # Data Explorer
            "Stick to your guns. No mid-game changes.",  # Reflexive Thinker
            "Blend both—acknowledge the shift but keep focus.",  # Balanced Strategist
            "Evaluate the shift for ethical implications.",  # Ethical Researcher
            "Analyze new data trends efficiently.",  # Efficient Innovator
            "Carefully assess risks of changing direction."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Data Explorer",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Ethical Researcher",
            "The Efficient Innovator",
            "The Risk-Conscious Analyst"
        ]
    },
    {
        "scenario": "The Interpretation Challenge",
        "description": (
            "AI’s sentiment analysis feels a bit...off. What’s your plan?"
        ),
        "options": [
            "Trust the numbers. Data knows best!",  # Efficient Innovator
            "Dig deeper—manual reanalysis time.",  # Reflexive Thinker
            "Combine AI’s stats with your qualitative genius.",  # Balanced Strategist
            "Explore the ambiguous cases for insights.",  # Data Explorer
            "Ensure ethical handling of borderline cases.",  # Ethical Researcher
            "Evaluate and address risks in misclassifications."  # Risk-Conscious Analyst
        ],
        "outcomes": [
            "The Efficient Innovator",
            "The Reflexive Thinker",
            "The Balanced Strategist",
            "The Data Explorer",
            "The Ethical Researcher",
            "The Risk-Conscious Analyst"
        ]
    }
]


outcome_descriptions = {
    "The Ethical Researcher": "You prioritize ethics and ensure participant confidentiality, advocating for marginalized voices and responsible AI use.",
    "The Efficient Innovator": "You fully leverage AI's potential to streamline processes, driving efficiency while maintaining high research quality.",
    "The Balanced Strategist": "You skillfully balance AI's capabilities with human intuition, merging speed with thoughtful depth in your research.",
    "The Reflexive Thinker": "You prioritize reflexivity, ensuring your research interpretations remain context-sensitive and grounded in qualitative traditions.",
    "The Data Explorer": "You are curious and open to unexpected insights, embracing new narratives and patterns that emerge from the data.",
    "The Risk-Conscious Analyst": "You carefully assess the risks and uncertainties of AI integration, ensuring data security and mitigating unintended consequences."
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
st.title("Victoria's Secret")

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