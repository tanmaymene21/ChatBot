from app.bot.graph import process_query

def test_chatbot():
    queries = [
        "Show me all products",
        "Show me all suppliers",
        "Show me all Electronics products",
        "What gaming products do you have?",
        "List all accessories",
        "Can I get a list of all furniture items?",
        "Show me all products under brand TechMaster"  
    ]
    
    for query in queries:
        separator = "=" * 50
        
        response = process_query(query)
        
        print(f"\n{separator}")
        print(f"Testing query: {query}")
        print(f"{separator}")
        print(f"\nResponse: {response}")
        print(f"{separator}\n")

if __name__ == "__main__":
    test_chatbot()