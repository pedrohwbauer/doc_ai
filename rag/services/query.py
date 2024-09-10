from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from .db import Database

async def query(question):
    db = Database.get_instance()
    print("\n--- Question ---")
    print(f"\n/{question}")

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )
    doc = (await retriever.ainvoke(question))[0]

    # Display the relevant results with metadata
    print(f"Document content:\n{doc}\n")
    
    combined_input = (
        "Here is a document that might help answer the question: "
        + question
        + "\n\nDocument content:\n"
        + f"\n\n{doc.page_content}"
        + "\n\nPlease provide an answer in the portuguese language based only on the provided document content. If the answer is not found in the document, respond with 'I'm not sure'."
    )
    
    model = ChatOpenAI(model="gpt-4o")

    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content=combined_input),
    ]

    result = model.invoke(messages)

    print("\n--- Generated Response ---")
    print(result)
    print("Content only:")
    print(result.content)
    
    return (result.content, doc.metadata)
