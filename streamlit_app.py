
import streamlit as st

# ==========================================
# INSIGHT - PERSONALITY SELF-REFLECTION APP
# ==========================================

st.set_page_config(
    page_title="INSIGHT | Understand Yourself",
    page_icon="🧠",
    layout="wide"
)

# ---------- DESIGN ----------

st.markdown("""
<style>
.stApp {
    background-color: #F4F7FB;
}

h1, h2, h3 {
    color: #172D42;
}

.hero {
    background-color: #172D42;
    padding: 30px;
    border-radius: 16px;
    color: white;
}

.hero h1 {
    color: white;
    font-size: 46px;
}

.hero p {
    color: #D9E2EC;
    font-size: 17px;
}

div.stButton > button {
    border-radius: 9px;
    min-height: 45px;
}

div.stButton > button[kind="primary"] {
    background-color: #2D9C91;
    border-color: #2D9C91;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------- PERSONALITY QUESTIONS ----------

questions = [
    ("I am the life of the party.", "Extraversion", False),
    ("I sympathize with others' feelings.", "Agreeableness", False),
    ("I get chores done right away.", "Conscientiousness", False),
    ("I have frequent mood swings.", "Neuroticism", False),
    ("I have a vivid imagination.", "Openness", False),

    ("I don't talk a lot.", "Extraversion", True),
    ("I am not interested in other people's problems.", "Agreeableness", True),
    ("I often forget to put things back in their proper place.", "Conscientiousness", True),
    ("I am relaxed most of the time.", "Neuroticism", True),
    ("I am not interested in abstract ideas.", "Openness", True),

    ("I talk to a lot of different people at parties.", "Extraversion", False),
    ("I feel others' emotions.", "Agreeableness", False),
    ("I like order.", "Conscientiousness", False),
    ("I get upset easily.", "Neuroticism", False),
    ("I have difficulty understanding abstract ideas.", "Openness", True),

    ("I keep in the background.", "Extraversion", True),
    ("I am not really interested in others.", "Agreeableness", True),
    ("I make a mess of things.", "Conscientiousness", True),
    ("I seldom feel blue.", "Neuroticism", True),
    ("I do not have a good imagination.", "Openness", True)
]

options = {
    "Very inaccurate": 1,
    "Moderately inaccurate": 2,
    "Neither inaccurate nor accurate": 3,
    "Moderately accurate": 4,
    "Very accurate": 5
}

descriptions = {
    "Extraversion": (
        "Reflects social engagement, talkativeness and energy "
        "in social situations."
    ),
    "Agreeableness": (
        "Reflects consideration for others, sympathy and "
        "interpersonal interest."
    ),
    "Conscientiousness": (
        "Reflects organisation, order and task completion."
    ),
    "Neuroticism": (
        "Reflects tendencies involving emotional sensitivity "
        "and negative emotional experiences."
    ),
    "Openness": (
        "Reflects imagination, interest in abstract ideas "
        "and intellectual curiosity."
    )
}


# ---------- SESSION STATE ----------

if "page" not in st.session_state:
    st.session_state.page = "home"

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "personality_results" not in st.session_state:
    st.session_state.personality_results = None


# ---------- HEADER ----------

st.markdown("""
<div class="hero">
    <h1>INSIGHT</h1>
    <p>Understand Yourself. Improve Yourself.</p>
    <p>Your journey towards self-awareness starts here.</p>
</div>
""", unsafe_allow_html=True)

st.write("")


# ==========================================
# DASHBOARD
# ==========================================

if st.session_state.page == "home":

    st.title("Welcome to INSIGHT")

    st.write(
        "Explore your personality, practise real-life situations "
        "and discover the skills you can strengthen."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🧠 Know Your Personality")
        st.write("Discover your Big Five personality profile.")

        if st.button(
            "Explore Personality",
            key="home_personality",
            use_container_width=True
        ):
            st.session_state.page = "personality"
            st.session_state.question_index = 0
            st.session_state.answers = {}
            st.rerun()

    with col2:
        st.subheader("🎯 Get Better")
        st.write("Practise responding to everyday challenges.")

        st.button(
            "Coming Soon",
            key="home_practice",
            disabled=True,
            use_container_width=True
        )

    with col3:
        st.subheader("📊 Know Your Weak Areas")
        st.write("Reflect on skills you want to strengthen.")

        st.button(
            "Coming Soon",
            key="home_skills",
            disabled=True,
            use_container_width=True
        )

    st.divider()

    st.subheader("How INSIGHT works")

    st.write("""
    1. **Discover:** Understand your personality.
    2. **Practise:** Learn from realistic situations.
    3. **Improve:** Identify skills you want to develop.
    """)


# ==========================================
# PERSONALITY ASSESSMENT
# ==========================================

elif st.session_state.page == "personality":

    st.title("🧠 Know Your Personality")

    st.write(
        "Answer honestly according to how you generally behave. "
        "There are no right or wrong answers."
    )

    st.info(
        "Choose the response that best describes you, "
        "rather than the person you wish to become."
    )

    index = st.session_state.question_index

    question, dimension, reverse = questions[index]

    st.progress((index + 1) / 20)

    st.caption(f"QUESTION {index + 1} OF 20")

    st.subheader(question)

    response_key = f"personality_response_{index}"

    previous_answer = st.session_state.answers.get(index)

    default_option = None

    if previous_answer is not None:
        for label, value in options.items():
            if value == previous_answer:
                default_option = label
                break

    option_list = list(options.keys())

    default_index = (
        option_list.index(default_option)
        if default_option is not None
        else None
    )

    selected = st.radio(
        "How accurately does this describe you?",
        option_list,
        index=default_index,
        key=response_key
    )

    st.write("")

    left, right = st.columns(2)

    with left:

        if index > 0:

            if st.button(
                "← Previous",
                key=f"previous_{index}",
                use_container_width=True
            ):

                st.session_state.answers[index] = options[selected]
                st.session_state.question_index -= 1
                st.rerun()

    with right:

        if index == 19:
            next_label = "Calculate My Results"
        else:
            next_label = "Next →"

        if st.button(
            next_label,
            key=f"next_{index}",
            type="primary",
            use_container_width=True
        ):

            if selected is None:
                st.warning("Please select an answer.")

            else:
                st.session_state.answers[index] = options[selected]

                if index < 19:
                    st.session_state.question_index += 1
                    st.rerun()

                else:
                    st.session_state.page = "results"
                    st.session_state.personality_results = None
                    st.rerun()

    st.divider()

    if st.button(
        "Cancel Assessment",
        key="cancel_personality"
    ):
        st.session_state.page = "home"
        st.session_state.question_index = 0
        st.session_state.answers = {}
        st.rerun()


# ==========================================
# PERSONALITY RESULTS
# ==========================================

elif st.session_state.page == "results":

    st.title("Your Personality Profile")

    if len(st.session_state.answers) != 20:

        st.error("Your assessment is incomplete.")

        if st.button(
            "Return to Assessment",
            key="return_incomplete"
        ):
            st.session_state.page = "personality"
            st.session_state.question_index = 0
            st.rerun()

    else:

        # Calculate scores only once
        if st.session_state.personality_results is None:

            dimensions = {
                "Extraversion": [],
                "Agreeableness": [],
                "Conscientiousness": [],
                "Neuroticism": [],
                "Openness": []
            }

            for i, (question, dimension, reverse) in enumerate(questions):

                score = st.session_state.answers[i]

                if reverse:
                    score = 6 - score

                dimensions[dimension].append(score)

            results = {}

            for dimension, scores in dimensions.items():

                results[dimension] = round(
                    sum(scores) / len(scores), 2
                )

            st.session_state.personality_results = results

        results = st.session_state.personality_results

        st.success("Your assessment is complete!")

        st.write(
            "Here is a summary of your responses across "
            "the five personality dimensions."
        )

        for dimension, score in results.items():

            st.subheader(dimension)

            st.write(descriptions[dimension])

            st.write(f"**Your score: {score} / 5**")

            st.progress(score / 5)

            st.write("")

        st.divider()

        st.subheader("Understanding Your Profile")

        st.write("""
        These five dimensions describe different aspects of personality.
        They are not measures of personal worth, intelligence or success.
        A higher score is not automatically better, and a lower score
        is not automatically worse.
        """)

        st.info(
            "This is an educational self-reflection result, "
            "not a clinical assessment or psychological diagnosis."
        )

        # Download results
        report = "INSIGHT - Personality Results\n\n"

        for dimension, score in results.items():
            report += f"{dimension}: {score}/5\n"

        st.download_button(
            "Download My Results",
            data=report,
            file_name="insight_personality_results.txt",
            mime="text/plain",
            key="download_personality"
        )

        if st.button(
            "Return to Dashboard",
            key="results_home",
            type="primary"
        ):
            st.session_state.page = "home"
            st.session_state.question_index = 0
            st.session_state.answers = {}
            st.session_state.personality_results = None
            st.rerun()


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "INSIGHT | An educational self-reflection project. "
    "Not medical advice, a psychological diagnosis, "
    "or a substitute for professional assessment."
)
