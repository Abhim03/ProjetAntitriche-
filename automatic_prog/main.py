from bots.junior_bot import JuniorBot
from bots.senior_bot import SeniorBot


def main():
    # Initialisation des bots
    junior_bot = JuniorBot()
    senior_bot = SeniorBot()

    problem_description = "calculer la somme de deux nombres"

    print("Solution générée par le Junior Bot:")
    junior_solution = junior_bot.generate_code(problem_description)
    print(junior_solution)

    print("\nSolution générée par le Senior Bot:")
    senior_solution = senior_bot.generate_code(problem_description)
    print(senior_solution)


if __name__ == "__main__":
    main()
