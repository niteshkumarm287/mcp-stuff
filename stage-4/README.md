Plan
├── stage_4_tools/                    # 🎯 Next - Tools & custom functions
│   ├── __init__.py
│   ├── agent.py                      # All tool-based agents
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── weather.py                # Custom weather tool
│   │   ├── finance.py                # Stock & mortgage tools
│   │   └── utils.py                  # Shared utilities
│   ├── tests/
│   │   ├── test_weather_agent.py
│   │   ├── test_research_agent.py
│   │   └── test_financial_agent.py
│   └── README.md


Test code - yet to be tested

"""
Stage 4: Comprehensive Tools & Custom Functions Implementation
Learn: Tool creation, Google Search, Code Execution, and Multi-tool agents
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search, code_execution
import json
from datetime import datetime
import random

# ============================================================================
# STAGE 4A: Custom Tools
# ============================================================================

def get_weather(city: str, units: str = "celsius") -> dict:
    """
    Retrieves the current weather report for a specified city.

    Args:
        city: The name of the city to get weather for
        units: Temperature units - 'celsius' or 'fahrenheit' (default: celsius)

    Returns:
        dict: A dictionary containing weather information with status and report
    """
    # Simulated weather data (in production, call a real API)
    weather_data = {
        "new york": {"temp": 25, "condition": "Sunny", "humidity": 65},
        "london": {"temp": 18, "condition": "Cloudy", "humidity": 78},
        "tokyo": {"temp": 28, "condition": "Rainy", "humidity": 85},
        "paris": {"temp": 22, "condition": "Partly Cloudy", "humidity": 70},
        "mumbai": {"temp": 32, "condition": "Hot and Humid", "humidity": 90},
    }

    city_lower = city.lower()
    if city_lower in weather_data:
        data = weather_data[city_lower]
        temp = data["temp"]

        # Convert to Fahrenheit if requested
        if units.lower() == "fahrenheit":
            temp = (temp * 9/5) + 32
            unit_str = "°F"
        else:
            unit_str = "°C"

        return {
            "status": "success",
            "report": f"The weather in {city.title()} is {data['condition']} with a temperature of {temp}{unit_str} and humidity of {data['humidity']}%.",
            "temperature": temp,
            "condition": data["condition"],
            "humidity": data["humidity"]
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available."
        }


def get_stock_price(symbol: str) -> dict:
    """
    Retrieves the current stock price for a given ticker symbol.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')

    Returns:
        dict: Stock information including price, change, and volume
    """
    # Simulated stock data
    stocks = {
        "AAPL": {"price": 178.50, "change": +2.3, "volume": "52.4M"},
        "GOOGL": {"price": 142.80, "change": -1.5, "volume": "28.1M"},
        "MSFT": {"price": 385.20, "change": +5.7, "volume": "31.2M"},
        "TSLA": {"price": 248.90, "change": -8.2, "volume": "112.3M"},
    }

    symbol_upper = symbol.upper()
    if symbol_upper in stocks:
        data = stocks[symbol_upper]
        change_str = f"+{data['change']}" if data['change'] > 0 else str(data['change'])

        return {
            "status": "success",
            "symbol": symbol_upper,
            "price": data["price"],
            "change": data["change"],
            "change_percent": f"{(data['change'] / data['price'] * 100):.2f}%",
            "volume": data["volume"],
            "report": f"{symbol_upper} is trading at ${data['price']} ({change_str} today) with volume {data['volume']}"
        }
    else:
        return {
            "status": "error",
            "error_message": f"Stock symbol '{symbol}' not found."
        }


def calculate_mortgage(
    loan_amount: float,
    annual_rate: float,
    years: int
) -> dict:
    """
    Calculates monthly mortgage payment and total interest.

    Args:
        loan_amount: The principal loan amount in dollars
        annual_rate: Annual interest rate as a percentage (e.g., 6.5 for 6.5%)
        years: Loan term in years

    Returns:
        dict: Monthly payment, total payment, and total interest calculations
    """
    try:
        monthly_rate = (annual_rate / 100) / 12
        num_payments = years * 12

        if monthly_rate == 0:
            monthly_payment = loan_amount / num_payments
        else:
            monthly_payment = loan_amount * (
                monthly_rate * (1 + monthly_rate) ** num_payments
            ) / ((1 + monthly_rate) ** num_payments - 1)

        total_payment = monthly_payment * num_payments
        total_interest = total_payment - loan_amount

        return {
            "status": "success",
            "loan_amount": f"${loan_amount:,.2f}",
            "annual_rate": f"{annual_rate}%",
            "loan_term": f"{years} years",
            "monthly_payment": f"${monthly_payment:,.2f}",
            "total_payment": f"${total_payment:,.2f}",
            "total_interest": f"${total_interest:,.2f}",
            "report": f"For a ${loan_amount:,.0f} loan at {annual_rate}% for {years} years, your monthly payment would be ${monthly_payment:,.2f}. Total interest: ${total_interest:,.2f}"
        }
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Calculation error: {str(e)}"
        }


# ============================================================================
# STAGE 4A: Weather Agent with Custom Tool
# ============================================================================

weather_agent = LlmAgent(
    name='weather_assistant',
    model='gemini-2.5-flash',
    description='A helpful assistant that provides weather information for cities worldwide.',
    instruction='''
    You are a friendly weather assistant. When users ask about weather:
    1. Use the get_weather tool to fetch current conditions
    2. Present the information in a natural, conversational way
    3. Offer relevant advice (e.g., "Don't forget an umbrella!" if rainy)
    4. If weather data is unavailable, apologize and suggest nearby cities

    Be helpful, accurate, and personable.
    ''',
    tools=[get_weather]
)


# ============================================================================
# STAGE 4B: Research Agent with Google Search
# ============================================================================

research_agent = LlmAgent(
    name='research_assistant',
    model='gemini-2.5-flash',
    description='An intelligent research assistant that can search the web for information.',
    instruction='''
    You are a skilled research assistant. When users ask questions:
    1. Use Google Search to find current, accurate information
    2. Synthesize information from multiple sources
    3. Cite your sources clearly
    4. Distinguish between facts and opinions
    5. If information conflicts, present different viewpoints

    Always be thorough, accurate, and cite your sources.
    ''',
    tools=[google_search]
)


# ============================================================================
# STAGE 4C: Code Analysis Agent with Code Execution
# ============================================================================

code_analyst_agent = LlmAgent(
    name='code_analyst',
    model='gemini-2.5-flash',
    description='An expert code analyst that can execute and analyze Python code.',
    instruction='''
    You are an expert Python developer and code analyst. When users share code:
    1. Analyze the code for correctness, efficiency, and best practices
    2. Use code execution to verify behavior and test edge cases
    3. Suggest improvements and optimizations
    4. Explain complex concepts clearly
    5. Write test cases to validate functionality

    Always prioritize code quality, security, and performance.
    ''',
    tools=[code_execution]
)


# ============================================================================
# STAGE 4D: Multi-Tool Financial Assistant
# ============================================================================

financial_agent = LlmAgent(
    name='financial_assistant',
    model='gemini-2.5-flash',
    description='A comprehensive financial assistant with stock prices, calculations, and research.',
    instruction='''
    You are a knowledgeable financial assistant. You can:
    1. Look up stock prices and provide market analysis
    2. Calculate mortgages and loans
    3. Research financial topics and news
    4. Execute code for complex financial calculations

    When helping users:
    - Use the appropriate tool for each task
    - Explain financial concepts clearly
    - Provide actionable insights
    - Always include disclaimers for investment advice

    Be professional, accurate, and helpful.
    ''',
    tools=[get_stock_price, calculate_mortgage, google_search, code_execution]
)


# ============================================================================
# STAGE 4E: Super Agent - All Tools Combined
# ============================================================================

super_agent = LlmAgent(
    name='super_assistant',
    model='gemini-2.5-flash',
    description='An all-purpose assistant with access to weather, stocks, calculations, search, and code execution.',
    instruction='''
    You are an incredibly versatile AI assistant with access to multiple tools:

    AVAILABLE TOOLS:
    - Weather: Get current conditions for any city
    - Stocks: Look up stock prices and market data
    - Mortgage Calculator: Calculate loan payments
    - Google Search: Research any topic
    - Code Execution: Run Python code for analysis

    BEST PRACTICES:
    1. Choose the right tool for each task
    2. Combine tools when needed (e.g., search for financial news, then look up stock prices)
    3. Explain your reasoning when using tools
    4. Provide comprehensive, well-structured answers
    5. Be proactive - suggest related information that might be helpful

    Always be helpful, accurate, and user-focused.
    ''',
    tools=[get_weather, get_stock_price, calculate_mortgage, google_search, code_execution]
)


# ============================================================================
# Root Agent for Testing
# ============================================================================

# Export the super_agent as root_agent for ADK CLI
root_agent = super_agent


# ============================================================================
# Example Usage & Testing
# ============================================================================

async def test_agents():
    """Test each agent with example queries"""

    print("=" * 80)
    print("STAGE 4: TOOLS & CUSTOM FUNCTIONS - TEST SUITE")
    print("=" * 80)

    # Test 4A: Weather Agent
    print("\n[TEST 4A] Weather Agent")
    print("-" * 40)
    response = await weather_agent.run("What's the weather in Tokyo?")
    print(f"Response: {response.get('content', 'No response')}")

    # Test 4B: Research Agent
    print("\n[TEST 4B] Research Agent")
    print("-" * 40)
    response = await research_agent.run("What are the latest developments in quantum computing?")
    print(f"Response: {response.get('content', 'No response')}")

    # Test 4C: Code Analyst
    print("\n[TEST 4C] Code Analysis Agent")
    print("-" * 40)
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print([fibonacci(i) for i in range(10)])
"""
    response = await code_analyst_agent.run(f"Analyze this code and suggest improvements:\n{test_code}")
    print(f"Response: {response.get('content', 'No response')}")

    # Test 4D: Financial Agent
    print("\n[TEST 4D] Financial Assistant (Multi-Tool)")
    print("-" * 40)
    response = await financial_agent.run(
        "What's the current price of AAPL? Also calculate monthly payments for a $500,000 mortgage at 6.5% for 30 years."
    )
    print(f"Response: {response.get('content', 'No response')}")

    # Test 4E: Super Agent
    print("\n[TEST 4E] Super Agent (All Tools)")
    print("-" * 40)
    response = await super_agent.run(
        "What's the weather in New York? Also look up GOOGL stock price and tell me about recent tech news."
    )
    print(f"Response: {response.get('content', 'No response')}")

    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_agents())