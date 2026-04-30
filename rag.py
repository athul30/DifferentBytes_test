import os
import chromadb
from groq import Groq
from dotenv import load_dotenv

# Load environment variables (gets GROQ_API_KEY from .env)
load_dotenv()

# 1. Initialize Groq Client

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
chroma_client = chromadb.Client() 
# Or use persistent: chromadb.PersistentClient(path="./chroma_db")

# Create a collection
collection = chroma_client.get_or_create_collection(name="rag_test_collection")

def add_to_knowledge_base(text: str, doc_id: str):
    """Adds a document to ChromaDB"""
    print(f"Ingesting document: {doc_id}...")
    collection.add(
        documents=[text],
        ids=[doc_id]
    )
    print("Done!")

def ask_question(query: str):
    """Searches ChromaDB and asks Groq the question"""
    print(f"\nQuestion: {query}")
    
    # Step 1: Retrieve context from ChromaDB
    results = collection.query(
        query_texts=[query],
        n_results=1 # get the top 1 most relevant document
    )
    
    retrieved_texts = results['documents'][0] if results['documents'] else []
    context = "\n\n".join(retrieved_texts)
    
    print(f"[Retrieved Context]: {context}")

    # Step 2: Build the prompt with context
    system_prompt = (
        "You are a helpful AI assistant. Use the provided context to answer the user's question. "
        "If the answer is not in the context, say 'I don't know based on the provided context.'\n\n"
        f"Context:\n{context}"
    )

    # Step 3: Generate answer using Groq
    print("\nAsking Groq...")
    completion = groq_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        model="openai/gpt-oss-120b",
        temperature=0.5,
    )
    
    answer = completion.choices[0].message.content
    print(f"\n[Answer]: {answer}")

if __name__ == "__main__":
    # --- DEMO ---
    
    # 1. Add some knowledge
    add_to_knowledge_base(
        text="Computer Science Engineering student with experience building AI pipelines, backend APIs, and NLP systems. Developed a real-time hallucination detection system using fine-tuned ModernBERT achieving 96%+ accuracy. Won HackSUS 5, a national-level hackathon. Currently interning at Innovature Labs.Computer Science Engineering student with experience building AI pipelines, backend APIs, and NLP systems. Developed a real-time hallucination detection system using fine-tuned ModernBERT achieving 96%+ accuracy. Won HackSUS 5, a national-level hackathon. Currently interning at Innovature Labs.",
        doc_id="profile"
    )
    add_to_knowledge_base(
        text="Python , C , Java",
        doc_id="programming_languages"
    )
    add_to_knowledge_base(
        text="HackSUS 5 is a national-level hackathon where teams compete to build innovative solutions. The candidate won this hackathon, showcasing their skills and creativity in problem-solving.",
        doc_id="hackathon"
    )

    add_to_knowledge_base(
        text="candidate is doing an internship at the company Innovature labs ",
        doc_id="internship"
    )
    add_to_knowledge_base(
        text="The candidate is doing his Btech at Rajagiri School of Engineering and Technology in Bangalore, India. He is currently in his 3rd year of study and is expected to graduate in 2025.",
        doc_id="education"
    )
    

    while(True):
        input_q=input("Enter the question that u want to ask?\n")

        ask_question(input_q)
        print("Do u wanna quit ?(0/1)")
        if input()=='1':
            break