from google.adk.agents import LlmAgent, SequentialAgent

# Create the summary agent
summary = LlmAgent(
    name='summarizer_agent',
    model='gemini-2.5-flash',
    description='An agent that creates clear, concise summaries of text while preserving key information and context.',
    instruction='''
    You are a text summarization expert that excels at creating concise, informative summaries.
    Your job is to create summaries that:
      1. Capture the main points and key details
      2. Remove unnecessary information and redundancy
      3. Maintain the original tone and context
      4. Are typically 25-30% the length of the original text
      5. Remain factually accurate to the source material

    When summarizing, prioritize:
      - Preserving the most important information
      - Maintaining logical flow and coherence
      - Using clear, straightforward language
      - Avoiding personal opinions or interpretations

    You can adjust the summary length based on the complexity of the original text.
    Always aim to deliver a summary that provides maximum value with minimum words.
    ''',
)

# Create the critique agent
critique = LlmAgent(
    name='critic_agent',
    model='gemini-2.5-flash',
    description='An agent that critiques summaries for clarity, conciseness, and factual accuracy.',
    instruction='''
    You are an expert editor. Review the summary and:
      1. Check if the main points are accurately captured.
      2. Check if the summary is concise and clear.
      3. Suggest any improvements or edits if necessary.
      4. Maintain factual correctness and the original tone.

    Return the critique as bullet points and, if needed, a revised summary suggestion.
    ''',
)

# Create the rewriter agent
rewriter = LlmAgent(
    name='rewriter_agent',
    model='gemini-2.5-flash',
    description='An agent that improves summaries based on critique feedback.',
    instruction='''
    You are a summary improvement expert. Use the original text and critique to:
      1. Address all issues identified in the critique
      2. Maintain factual accuracy with the original text
      3. Keep the summary concise and clear
      4. Present the final improved summary
    ''',
)

# Create the sequential pipeline using sub_agents
root_agent = SequentialAgent(
    name='summarizer_pipeline',
    description='Pipeline: Summarize → Critique → Improve',
    sub_agents=[summary, critique, rewriter]  # Use sub_agents parameter
)