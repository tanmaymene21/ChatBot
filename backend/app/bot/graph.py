import os
from typing import TypedDict, Annotated, Sequence, List, Dict, Any
from enum import Enum
import json
import logging
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_core.messages import AIMessage
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

from app.models.product import Product
from app.models.supplier import Supplier
from app.db.database import get_db

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY environment variable is required")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], add_messages]
    query_type: str
    entities: dict

llm = ChatGroq(
    model="mixtral-8x7b-32768",  
    temperature=0.2,
    api_key=GROQ_API_KEY
)

@tool
def search_products(query: str = "", filters: dict = None) -> str:
    """
    Search for products in the database with optional filters.
    
    Args:
        query: Search query string
        filters: Dictionary of filters including category, price range, brand, etc.
        
    Returns:
        JSON string containing matched products and count
    """
    db = next(get_db())
    
    try:
        stmt = select(Product)
        if filters:
            for key, value in filters.items():
                if value and hasattr(Product, key):
                    if key == 'category':
                        stmt = stmt.where(Product.category.ilike(f"%{value}%"))
                    elif key == 'max_price':
                        stmt = stmt.where(Product.price <= float(value))
                    elif key == 'min_price':
                        stmt = stmt.where(Product.price >= float(value))
                    elif key in ['name', 'brand']:
                        stmt = stmt.where(getattr(Product, key).ilike(f"%{value}%"))
                    else:
                        stmt = stmt.where(getattr(Product, key) == value)
        
        products = db.execute(stmt).scalars().all()
        
        result = {
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "price": p.price,
                    "category": p.category,
                    "description": p.description,
                    "supplier_id": p.supplier_id
                } for p in products
            ],
            "count": len(products)
        }
        return json.dumps(result)
    except Exception as e:
        logger.error(f"Error searching products: {str(e)}")
        return json.dumps({"error": str(e)})
    finally:
        db.close()

@tool
def get_product_details(product_id: int) -> str:
    """
    Get detailed information about a specific product.
    
    Args:
        product_id: The ID of the product to retrieve
        
    Returns:
        JSON string containing product details
    """
    db = next(get_db())
    
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product:
            return json.dumps({"error": f"Product with ID {product_id} not found"})
            
        result = {
            "id": product.id,
            "name": product.name,
            "brand": product.brand,
            "price": product.price,
            "category": product.category,
            "description": product.description,
            "supplier_id": product.supplier_id
        }
        
        return json.dumps(result)
    
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        db.close()

@tool
def search_suppliers(query: str, filters: dict = None) -> str:
    """
    Search for suppliers in the database with optional filters.
    
    Args:
        query: Search query string
        filters: Dictionary of filters including category, name, etc.
        
    Returns:
        JSON string containing matched suppliers and count
    """
    db = next(get_db())
    
    try:
        stmt = select(Supplier)
        
        if filters:
            if "category" in filters and filters["category"]:
                stmt = stmt.where(Supplier.categories_offered.contains([filters["category"]]))
            if "name" in filters and filters["name"]:
                stmt = stmt.where(Supplier.name.ilike(f"%{filters['name']}%"))
        
        elif query:
            stmt = stmt.where(
                (Supplier.name.ilike(f"%{query}%")) | 
                (Supplier.email.ilike(f"%{query}%")) |
                (Supplier.address.ilike(f"%{query}%"))
            )
        
        suppliers = db.execute(stmt).scalars().all()
        
        if not suppliers:
            return json.dumps({"suppliers": [], "count": 0, "message": "No suppliers found matching your criteria."})
            
        result = {
            "suppliers": [
                {
                    "id": s.id,
                    "name": s.name,
                    "email": s.email,
                    "phone": s.phone,
                    "address": s.address,
                    "categories_offered": s.categories_offered
                } for s in suppliers
            ],
            "count": len(suppliers)
        }
        
        return json.dumps(result)
    
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        db.close()

@tool
def get_supplier_details(supplier_id: int) -> str:
    """
    Get detailed information about a specific supplier.
    
    Args:
        supplier_id: The ID of the supplier to retrieve
        
    Returns:
        JSON string containing supplier details and products count
    """
    logger.info(f"Fetching supplier details for ID: {supplier_id}")
    db = next(get_db())
    
    try:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not supplier:
            return json.dumps({"error": "Supplier not found"})
            
        # Get supplier's products
        products = db.query(Product).filter(Product.supplier_id == supplier_id).all()
        
        result = {
            "supplier": {
                "id": supplier.id,
                "name": supplier.name,
                "email": supplier.email,
                "phone": supplier.phone,
                "address": supplier.address,
                "categories_offered": supplier.categories_offered,
                "products_count": len(products)
            }
        }
        return json.dumps(result)
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        db.close()

@tool
def get_supplier_products(supplier_id: int) -> str:
    """
    Get all products from a specific supplier.
    
    Args:
        supplier_id: The ID of the supplier whose products to retrieve
        
    Returns:
        JSON string containing supplier info and their products
    """
    db = next(get_db())
    
    try:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        
        if not supplier:
            return json.dumps({"error": f"Supplier with ID {supplier_id} not found"})
        
        products = db.query(Product).filter(Product.supplier_id == supplier_id).all()
        
        result = {
            "supplier": {
                "id": supplier.id,
                "name": supplier.name
            },
            "products": [
                {
                    "id": p.id,
                    "name": p.name,
                    "brand": p.brand,
                    "price": p.price,
                    "category": p.category,
                    "description": p.description
                } for p in products
            ],
            "count": len(products)
        }
        
        return json.dumps(result)
    
    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        db.close()

def query_analyzer(state: AgentState) -> AgentState:
    human_message = state["messages"][-1]
    query = human_message.content
    
    system_prompt = """
    You are a product and supplier query analyzer. Analyze the user query and determine:
    1. Query type (choose one):
        - 'product_search': For finding products with filters
        - 'product_details': For specific product information
        - 'supplier_search': For finding suppliers
        - 'supplier_details': For specific supplier information
        - 'supplier_products': For finding products from a specific supplier
    
    2. Extract all relevant entities including:
        - category: Product category (electronics, gaming, accessories, etc.)
        - min_price: Minimum price filter
        - max_price: Maximum price filter
        - brand: Product brand name
        - name: Product or supplier name
        - sort: Sorting preference (price_asc, price_desc)
        - supplier_name: Name of supplier
        - product_type: Specific type of product (laptop, keyboard, etc.)
    
    Return a JSON with:
    {
        "query_type": "<type>",
        "entities": {
            "category": "<category>",
            "min_price": <number or null>,
            "max_price": <number or null>,
            "brand": "<brand>",
            "name": "<name>",
            "sort": "<sort_preference>",
            "supplier_name": "<supplier>",
            "product_type": "<type>"
        }
    }
    
    Example 1: "Find me a gaming monitor under $500"
    {
        "query_type": "product_search",
        "entities": {
            "category": "gaming",
            "product_type": "monitor",
            "max_price": 500
        }
    }
    
    Example 2: "Show me all products from TechMaster sorted by price"
    {
        "query_type": "supplier_products",
        "entities": {
            "supplier_name": "TechMaster",
            "sort": "price_asc"
        }
    }
    """
    
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=query)
        ]
        
        response = llm.invoke(messages)
        analysis = json.loads(response.content)
        
        state["query_type"] = analysis["query_type"]
        state["entities"] = analysis["entities"]
        
    except Exception as e:
        logger.error(f"Query analysis error: {str(e)}")
        state["query_type"] = "product_search"
        state["entities"] = {}
    
    return state

def execute_db_query(state: AgentState) -> AgentState:
    try:
        query_type = state["query_type"]
        entities = state["entities"]
        result = None
        
        if query_type == "product_search":
            filters = {}
            if "category" in entities and entities["category"]:
                filters["category"] = entities["category"]
            if "max_price" in entities and entities["max_price"]:
                filters["max_price"] = entities["max_price"]
            if "min_price" in entities and entities["min_price"]:
                filters["min_price"] = entities["min_price"]
            if "brand" in entities and entities["brand"]:
                filters["brand"] = entities["brand"]
            if "product_type" in entities and entities["product_type"]:
                filters["name"] = entities["product_type"]
                
            result = search_products.invoke({"query": "", "filters": filters})
            
        elif query_type == "supplier_search":
            filters = {}
            if "category" in entities:
                filters["category"] = entities["category"]
            if "name" in entities:
                filters["name"] = entities["name"]
                
            result = search_suppliers.invoke({"query": "", "filters": filters})
            
        elif query_type == "supplier_details":
            if "supplier_name" in entities:
                supplier_results = json.loads(
                    search_suppliers.invoke({
                        "query": "", 
                        "filters": {"name": entities["supplier_name"]}
                    })
                )
                if supplier_results.get("suppliers") and len(supplier_results["suppliers"]) > 0:
                    supplier_id = supplier_results["suppliers"][0]["id"]
                    result = get_supplier_details.invoke({"supplier_id": supplier_id})
            
        elif query_type == "supplier_products":
            if "supplier_name" in entities:
                supplier_results = json.loads(
                    search_suppliers.invoke({
                        "query": "", 
                        "filters": {"name": entities["supplier_name"]}
                    })
                )
                if supplier_results.get("suppliers") and len(supplier_results["suppliers"]) > 0:
                    supplier_id = supplier_results["suppliers"][0]["id"]
                    result = get_supplier_products.invoke({"supplier_id": supplier_id})
                    
        if result:
            state["messages"].append(AIMessage(content=result))
        else:
            state["messages"].append(AIMessage(content=json.dumps({
                "error": "No results found for your query"
            })))
            
    except Exception as e:
        state["messages"].append(AIMessage(content=json.dumps({
            "error": "An error occurred while processing your request"
        })))
    
    return state

def summarize_results(state: AgentState) -> AgentState:
    try:
        data_message = state["messages"][-1]
        data = json.loads(data_message.content)
        
        if "error" in data:
            state["messages"][-1] = AIMessage(content=json.dumps(data))
            return state
            
        state["messages"][-1] = AIMessage(content=json.dumps(data))
        
    except Exception as e:
        state["messages"].append(AIMessage(content=json.dumps({
            "error": "An error occurred while processing the results"
        })))
    
    return state

def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)
    
    workflow.add_node("query_analyzer", query_analyzer)
    workflow.add_node("execute_db_query", execute_db_query)
    workflow.add_node("summarize_results", summarize_results)
    
    workflow.add_edge("query_analyzer", "execute_db_query")
    workflow.add_edge("execute_db_query", "summarize_results")
    workflow.add_edge("summarize_results", END)
    
    workflow.set_entry_point("query_analyzer")
    
    return workflow.compile()

chatbot_graph = build_graph()

def process_query(query: str) -> str:
    try:
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "query_type": "",
            "entities": {}
        }
        
        final_state = chatbot_graph.invoke(initial_state)
        final_message = final_state["messages"][-1]
        
        if isinstance(final_message, AIMessage):
            return final_message.content
            
    except Exception:
        return json.dumps({
            "error": "An error occurred while processing your request"
        })
    
    return json.dumps({
        "error": "Could not understand your request"
    })