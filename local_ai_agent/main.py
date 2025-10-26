from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from vector import retriever

model = OllamaLLM(model="llama3:latest")

template = """
You are an expert Python programmer. Answer the following question as best as you can. You have access to the internet so you can look up information if needed.

here is the question to answer: {input}

"""

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | model


while True:
    user_input = input("Ask your question: ")
    if user_input.lower() in ("exit", "quit"):
        break

    reviews = retriever.invoke({"query": user_input})
    print("Retrieved reviews:", reviews)

    result = chain.invoke({"input": user_input})
    print(result)
