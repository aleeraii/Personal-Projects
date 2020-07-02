class Question:
    def __init__(self, question, ans1, ans2, ans3, ans4, correct_ans):
        self.__ques = question
        self.__ans1 = ans1
        self.__ans2 = ans2
        self.__ans3 = ans3
        self.__ans4 = ans4
        self.__corr_ans = correct_ans

    def set_question(self, question):
        self.__ques = question
    def set_answer1(self, ans1):
        self.__ans1 = ans1
    def set_answer2(self, ans2):
        self.__ans1 = ans2
    def set_answer3(self, ans3):
        self.__ans1 = ans3
    def set_answer4(self, ans4):
        self.__ans1 = ans4
    def set_correct_answer(self, correct_ans):
        self.__corr_ans = correct_ans

    def get_question(self):
        return self.__ques
    def get_answer1(self):
        return self.__ans1
    def get_answer2(self):
        return self.__ans1
    def get_answer3(self):
        return self.__ans1
    def get_answer4(self):
        return self.__ans1
    def get_correct_answer(self):
        return self.__corr_ans


    def ask_question(self):
        print('Question: ' + self.__ques +
              '\nAnswers: ' +
              '\n1.' + self.__ans1 +
              '\n2.' + self.__ans2 +
              '\n3.' + self.__ans3 +
              '\n4.' + self.__ans4)


def play_game(question_objs):
    plyr1_correct = 0
    plyr2_correct = 0

    print("\nTrivia Quiz\n")
    for i in range(10):
        if i%2 == 0:
            print("\nPlayer 1's Turn:")
            question_objs[i].ask_question()
            choice = int(input("Enter Your Choice(1-4): "))
            if choice == question_objs[i].get_correct_answer():
                plyr1_correct += 1
        else:
            print("\nPlayer 2's Turn:")
            question_objs[i].ask_question()
            choice = int(input("Enter Your Choice(1-4): "))
            if choice == question_objs[i].get_correct_answer():
                plyr2_correct += 1
    print("Player 1's Score: ", plyr1_correct)
    print("Player 2's Score: ", plyr2_correct)
    if plyr1_correct > plyr2_correct:
        print("Player 1 Wins!")
    elif plyr2_correct > plyr1_correct:
        print("Player 2 Wins!")
    else:
        print("It's A Draw")


def main():
    question_bank = []
    answer_bank = [1,1,3,2,1,2,4,1,2,2]
    f = open('data/test', 'r')
    data = f.read().split('-')
    data.pop(0)
    for i in range(10):
        li1 = data[i].split('\n')
        ques = li1[0]
        ans1 = li1[1]
        ans2 = li1[2]
        ans3 = li1[3]
        ans4 = li1[4]
        question = Question(ques, ans1, ans2, ans3, ans4, answer_bank[i])
        question_bank += [question]

    play_game(question_bank)


main()