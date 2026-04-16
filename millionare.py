import json
import random

class Millionaire:
    index_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3}

    def __init__(self):
        self.data = []
        self.balance = 0
        self.question_no = 0
        with open("questions.json") as questions:
            self.data = json.load(questions)

    def start_of_game(self):
        name = input(f"input Your Name: ")
        print(f"Hello {name} and Welcome to Who Wants To Be A Millionaire", end='\n\n')


    def questions(self):
        self.easy = self.data[:101]
        random.shuffle(self.easy)
        self.medium = self.data[100:201]
        random.shuffle(self.medium)
        self.hard = self.data[200:]
        random.shuffle(self.hard)

    def choose(self):
        if 0 <= self.question_no <= 3:
            if len(self.easy) > 0:
                index = random.randrange(len(self.easy))
                return self.easy.pop(index)
        elif 3 < self.question_no <= 7:
            if len(self.medium) > 0:
                index = random.randrange(len(self.medium))
                return self.medium.pop(index)
        else:
            if len(self.hard) > 0:
                index = random.randrange(len(self.hard))
                return self.hard.pop(index)
        return []
    
    def display(self, question):
        print(question['question'],end='\n\n')
        answers = question['incorrectAnswers'].copy()
        answers.append(question['correctAnswer'])
        random.shuffle(answers)
        print(f"Choose one option from Possible Answers")
        print(f"A. {answers[0]} B. {answers[1]} C. {answers[2]} D. {answers[3]}",end='\n\n')
        return answers
    
    def answer(self):
        return input(f"Answer: ")
    
    def control(self, answer):
        if answer.lower() not in ['a', 'b', 'c', 'd']:
            print(f"{answer} is not a valid option, Choose Again!")
            return False
        return True
    
    def colour_options(self,question,answers, answer):
        options = [f"A. {answers[0]} ", f"B. {answers[1]} ", f"C. {answers[2]} ", f"D. {answers[3]}"]
        final = ""
        index = self.index_dict[answer.upper()]
        if answers[index] != question['correctAnswer']:
            options[index] = (f"\033[31m{options[index]}\033[0m")

        for i in range(len(options)):
            if answers[i] == question['correctAnswer']:
                final += (f"\033[32m{options[i]}\033[0m")
            else:
                final += options[i]
        return final
    
    def display_correct_answers(self, final):
        print(f"The Correct Answer: ")
        print(final)

    def check(self,question,answers, answer):
        if answers[self.index_dict[answer.upper()]] != question['correctAnswer']:
            return False
        else:
            return True

    def winnings(self):
        current = self.balance
        money = [2000, 5000,20000, 50000,150000,250000, 500]
        
        if self.balance == money[0]:
            self.balance = money[1]
        elif self.balance == money[2]:
            self.balance = money[3]
        elif self.balance == money[4]:
            self.balance = money[5]
        elif self.balance == 0:
            self.balance += money[6]
        else:
            self.balance *= 2
        print(f"Congratulations! You have Won {self.balance - current}$.",end='\n\n')

    def guaranteed(self):
        if self.balance in [1000, 50000]:
            print(f"\033[33mGood Job!. You now have {self.balance} Guaranteed\033[0m", end='\n\n')
    
    def lost(self):
        money = [50000, 1000]
        if self.balance >= money[0]:
            self.balance = money[0]
        elif self.balance >= money[1]:
            self.balance = money[1]
        else:
            self.balance = 0
        print(f"Game Over! You have won {self.balance}$. Thank You for playing.")

    def choice(self):
        print(f"You want to take the money or Continue playing: ")
        return input(f"(Take or Continue): ")
    
    def control_2(self, answer):
        if answer.lower() not in ['take', 'continue']:
            print(f"{answer} is not a valid option, Choose Again!")
            return False
        return True
    
    def termination(self, choice):
            if choice.lower() == 'take':
                print(f"Congratulations! You have won {self.balance}$. Thank You for playing.")
                return True
            return False

    def play(self):
        self.questions()
        self.start_of_game()
        while self.balance < 1000000:
            self.question_no += 1
            print(f"BALANCE: {self.balance}$.",end='\n\n')
            question = self.choose()
            options = self.display(question)
            answer = self.answer()
            print('\n')
            control_1 = self.control(answer)
            while not control_1:
                answer = self.answer()
                control_1 = self.control(answer)
            status = self.check(question, options, answer)
            colored = self.colour_options(question,options, answer)
            self.display_correct_answers(colored)
            if status == True:
                self.winnings()
                print(f"BALANCE: {self.balance}$.")
                self.guaranteed()
                choice = self.choice()
                print('\n')
                control_2 = self.control_2(choice)
                while not control_2:
                    choice = self.choice()
                    control_2 = self.control_2(choice)
                termination = self.termination(choice)
                if termination:
                    return
                if self.balance == 1000000:
                    print(f"Congratulations! You have won {self.balance}$. YOU ARE A MILLIONAiRE!!!.")
                    return
            else:
                self.lost()
                return



game = Millionaire()
game.play()        
