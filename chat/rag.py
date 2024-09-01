from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

def ask(db, query):
    print("\n--- Query ---")
    print(f"\n/{query}")
    # Retrieve relevant documents based on the query
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )
    relevant_docs = retriever.invoke(query)

    # Display the relevant results with metadata
    print("\n--- Relevant Documents ---")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"Document {i}:\n{doc.page_content}\n")

    # Combine the query and the relevant document contents
    combined_input = (
        "Here are some texts that might help answer the question: "
        + query
        + "\n\nRelevant texts:\n"
        + "\n\n".join([doc.page_content for doc in relevant_docs])
        + "\n\nPlease provide an answer based only on the provided texts. If the answer is not found in the texts, respond with 'I'm not sure'."
    )

    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")

    # Define the messages for the model
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=combined_input),
    ]

    # Invoke the model with the combined input
    result = model.invoke(messages)

    # Display the full result and content only
    print("\n--- Generated Response ---")
    # print("Full result:")
    # print(result)
    print("Content only:")
    print(result.content)

    return result.content