import openai
import streamlit as st

# Set up OpenAI API credentials
openai.api_key = st.secrets["openai_key"]

# Define the Streamlit app
def main():
    # Set page title and description
    st.set_page_config(page_title="Text Summarizer", page_icon="📖", layout="wide")
    st.title("Text Summarizer")
    st.write("Enter the long text you want to summarize below, and select the desired length of the summary, then click the button to summarize it.")

    # Create input field for user to enter text
    text_input = st.text_area("Input Text")

    # Create input field for user to specify length of summary
    summary_length = st.slider("Length of Summary", min_value=20, max_value=200, value=50, step=10)

    # Create button to summarize text
    if st.button("Summarize"):
        # Call OpenAI GPT-3 API to summarize the input text
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"Please summarize the following text:\n{text_input}\nSummary:",
                max_tokens=summary_length,
                n=1,
                top_p=1,
                stop=None,
                temperature=0.7,
                frequency_penalty=0,
                presence_penalty=0
            )
            summary = response.choices[0].text.strip()

            # Ensure that summary ends with a full sentence
            if summary[-1] not in [".", "!", "?"]:
                for i in range(len(summary)-1, 0, -1):
                    if summary[i] in [".", "!", "?"]:
                        summary = summary[:i+1]
                        break
        except Exception as e:
            st.write(f"Error: {e}")
            return

        # Display the summarized text
        st.subheader("Summary")
        st.write(summary)

# Run the app
if __name__ == "__main__":
    main()
