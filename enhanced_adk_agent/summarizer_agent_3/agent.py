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

    Output your summary in the following format:
    SUMMARY:
    [Your summary here]
    ''',
)

# Enhanced critique agent with scoring
critique = LlmAgent(
    name='critic_agent',
    model='gemini-2.5-flash',
    description='An agent that critiques summaries with numeric scoring for accuracy, clarity, and conciseness.',
    instruction='''
    You are an expert editor and evaluator. Review the summary and provide:

    1. NUMERIC SCORES (0-10 scale):
       - Accuracy: How well does it capture the original meaning?
       - Clarity: How clear and understandable is it?
       - Conciseness: How efficiently does it convey information?

    2. OVERALL QUALITY SCORE: Average of the three scores

    3. DETAILED CRITIQUE: Bullet points on:
       - What works well
       - What needs improvement
       - Specific suggestions for enhancement

    4. IMPROVEMENT PRIORITY: HIGH, MEDIUM, or LOW based on overall score

    Output format:
    SCORES:
    Accuracy: [X/10]
    Clarity: [X/10]
    Conciseness: [X/10]
    Overall Quality: [X/10]

    PRIORITY: [HIGH/MEDIUM/LOW]

    CRITIQUE:
    - [Point 1]
    - [Point 2]
    - [Point 3]

    SUGGESTED IMPROVEMENTS:
    - [Improvement 1]
    - [Improvement 2]
    ''',
)

# Fact-checker agent (optional enhancement)
fact_checker = LlmAgent(
    name='fact_checker_agent',
    model='gemini-2.5-flash',
    description='An agent that verifies factual accuracy between the summary and original text.',
    instruction='''
    You are a meticulous fact-checker. Compare the summary against the original text and:

    1. Identify any factual discrepancies or misrepresentations
    2. Flag information that's present in the original but missing from the summary
    3. Highlight any additions or interpretations not in the original
    4. Verify that numbers, names, dates, and specific details are accurate

    Output format:
    FACT-CHECK STATUS: [PASS/NEEDS REVIEW/FAIL]

    VERIFIED FACTS:
    - [Fact 1: Accurate]
    - [Fact 2: Accurate]

    DISCREPANCIES FOUND:
    - [Issue 1: Description]
    - [Issue 2: Description]

    MISSING KEY INFORMATION:
    - [Missing point 1]
    - [Missing point 2]

    RECOMMENDATIONS:
    - [Recommendation 1]
    ''',
)

# Enhanced rewriter with multi-pass capability
rewriter = LlmAgent(
    name='rewriter_agent',
    model='gemini-2.5-flash',
    description='An agent that improves summaries based on critique, scores, and fact-checking feedback.',
    instruction='''
    You are a summary improvement expert. Use ALL feedback provided to create an enhanced summary.

    Review:
    1. The original summary
    2. The critique scores and feedback
    3. The fact-checking results (if available)

    Then create an improved summary that:
    - Addresses all issues identified in the critique
    - Corrects any factual discrepancies
    - Maintains or improves all scores (Accuracy, Clarity, Conciseness)
    - Remains factually accurate to the original text
    - Keeps the summary concise and clear

    Output format:
    IMPROVED SUMMARY:
    [Your enhanced summary here]

    CHANGES MADE:
    - [Change 1]
    - [Change 2]
    - [Change 3]

    EXPECTED SCORE IMPROVEMENT:
    - Accuracy: [Expected improvement]
    - Clarity: [Expected improvement]
    - Conciseness: [Expected improvement]
    ''',
)

# Secondary rewriter for low-scoring summaries
secondary_rewriter = LlmAgent(
    name='secondary_rewriter_agent',
    model='gemini-2.5-flash',
    description='A second-pass rewriter for summaries that need additional refinement.',
    instruction='''
    You are performing a SECOND PASS refinement on a summary that still needs improvement.

    This summary has already been rewritten once but requires further enhancement.
    Focus on:
    1. Polish and refinement
    2. Eliminating any remaining issues
    3. Achieving excellence in all quality metrics
    4. Ensuring the summary is production-ready

    Output format:
    FINAL REFINED SUMMARY:
    [Your polished summary here]

    FINAL REFINEMENTS:
    - [Refinement 1]
    - [Refinement 2]
    ''',
)

# Create the advanced sequential pipeline
root_agent = SequentialAgent(
    name='summarizer_pipeline_advanced',
    description='Advanced Pipeline: Summarize → Fact-Check → Critique with Scoring → Conditional Multi-Pass Rewriting',
    sub_agents=[summary, fact_checker, critique, rewriter]
)