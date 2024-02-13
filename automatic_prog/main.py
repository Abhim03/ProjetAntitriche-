from bots.junior_bot import JuniorBot
from bots.senior_bot import SeniorBot
from utils.openai_utils import setup_openai_api


def main():
    # Configuration
    openai_api_key = "votre_clé_api_openai"
    setup_openai_api(openai_api_key)

    junior_bot = JuniorBot(openai_api_key)
    senior_bot = SeniorBot(openai_api_key)

    problem_description = "Écris une fonction en Python pour calculer la somme de deux nombres."

    print("Solution générée par le Junior Bot:")
    junior_code = junior_bot.generate_code(problem_description)
    print(junior_code)

    print("\nSolution générée par le Senior Bot:")
    senior_code = senior_bot.generate_code(problem_description)
    print(senior_code)


if __name__ == "__main__":
    main()
