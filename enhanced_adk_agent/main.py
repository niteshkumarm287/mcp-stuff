from .agent import root_agent

def main():
    text = "The Taj Mahal, located in Agra, Uttar Pradesh, was commissioned by Shah Jahan in memory of Mumtaz Mahal."
    result = root_agent.run(text)
    print("Stage 3 Pipeline Output:")
    print(result)

if __name__ == "__main__":
    main()
