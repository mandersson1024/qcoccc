from engine.flow import QuestionFlow
from questions.era import EraQuestion
from questions.occupation import OccupationQuestion
from questions.age_bracket import AgeBracketQuestion
from questions.age import AgeQuestion
from questions.output import OutputQuestion


def main():
    flow = QuestionFlow(questions=[
        EraQuestion(),
        OccupationQuestion(),
        AgeBracketQuestion(),
        AgeQuestion(),
        OutputQuestion(),
    ])
    context = flow.run()


if __name__ == "__main__":
    main()
