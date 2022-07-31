from __future__ import division
import quizapi
import os
import time
import random


class Quiz():
    def __init__(self):
        self.url = 'https://cae-bootstore.herokuapp.com'
        self.correct = 0.0
        self.score = 0.0


    def register(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Registration')
        email = input("Email:\n ")
        first_name = input("First Name:\n")
        last_name = input("Last Name:\n")
        password = input("Password:\n")       
        user_dict={
            "email":email,
            "first_name":first_name,
            "last_name":last_name,
            "password":password
        }
        return quizapi.register_user(user_dict)


    def login(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        email = input('Email Address:\n')
        password = input('Password:\n')
        self.user = quizapi.login_user(email, password) 
        return self.user


    def guest(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('*** Guest ***')
        print(f"Welcome, {self.user['first_name']}!")
        while True:
            prompt = input('''
1. The Quiz of All Quizes
2. Run While You Still Can... (Quit)
            \n''')
            if prompt == '1':
                self.take_quiz()
            elif prompt == '2':
                break

    def admin(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('*** Admin ***')
        print('')
        print(f"Welcome, {self.user['first_name']}!")
        while True:
            prompt = input('''
Choose Thy Fate:
1. Take The Quiz
2. See All Questions
3. See My Questions
4. Edit My Questions
5. Create A Question
6. Delete A Question 
7. Quit
            \n''')
            if prompt == '1':
                self.take_quiz()
            elif prompt == '2':
                self.show_all_questions()
            elif prompt == '3':
                self.show_my_questions()
            elif prompt == '4':
                self.edit_my_questions()
            elif prompt == '5':
                self.create_question()
            elif prompt == '6':
                self.delete_a_question()
            elif prompt == '7':
                #quit()
                break
            else:
                print('*** INVALID OPTION ***')


    def show_all_questions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('All Questions')
        self.all_questions = quizapi.get_all_questions(self.user['token'])
        for question in self.all_questions:
            print(question['question'])


    def show_my_questions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('My Questions:')
        self.my_questions = quizapi.get_my_questions(self.user['token'])
        self.author = self.user['first_name'] + ' ' + self.user['last_name'] + '_' + str(0) + str(self.user['user_id'])
        self.my_list_questions = []
        for question in self.my_questions:
            if question['author'] == self.author:
                self.my_list_questions.append(question['question'])
                print(question['question'])


    def edit_my_questions(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.my_questions = quizapi.get_my_questions(self.user['token'])
        self.author = self.user['first_name'] + ' ' + self.user['last_name'] + '_' + str(0) + str(self.user['user_id'])

        for question in self.my_questions:
            if question['author'] == self.author:
                print(f"Question: {question['question']}")
                print(f"Answer: {question['answer']}")
                print(f"ID: {question['id']}")
        print(self.my_questions[0]['id'])
        prompt = input('Enter The Question ID You Wish To Edit:.\n')
        revised_question = input('Enter Edited Question: \n')
        revised_answer = input('Enter Edited Answer:\n')
        question_dict={
            'question': revised_question,
            'answer': revised_answer
        }
        return(quizapi.edit_my_question(self.user['token'], prompt, question_dict))


    def delete_a_question(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.my_questions = quizapi.get_my_questions(self.user['token'])
        self.author = self.user['first_name'] + ' ' + self.user['last_name'] + '_' + str(0) + str(self.user['user_id'])

        for question in self.my_questions:
            if question['author'] == self.author:
                print(f"Question: {question['question']}")
                print(f"Answer: {question['answer']}")
                print(f"ID: {question['id']}")
        prompt = input('Enter The Question ID You Wish To Delete:\n')
        quizapi.delete_question(self.user['token'], prompt)


    def create_question(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        question = input('Enter Question:\n')
        answer = input('Enter Answer:\n')
        question_dict={
            'question': question,
            'answer': answer
        }
        return quizapi.create_question(self.user['token'], question_dict)


    def take_quiz(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.all_questions = quizapi.get_all_questions(self.user['token'])
        length_of_quiz = 10
        for x in range(10):
            random_integer = random.randint(0, len(self.all_questions)-1)
            random_question = (self.all_questions[random_integer]['question'])
            correct_answer = (self.all_questions[random_integer]['answer'])
            response = input(random_question)
            if response.lower() == correct_answer.lower():
                print(f"Correctamundo, {self.user['first_name']}!!")
                self.correct += 1
                time.sleep(2)
            else:
                print(f'Too Bad - So Sad - That is Incorrect! The Correct Answer is {correct_answer}\n')
                print(f'The Correct Answer is {correct_answer}')
                time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        score = round(self.correct / float(length_of_quiz), 2) * 100
        print('***************************************************************')
        print(f"You scored {self.correct} out of 10.0!\n")
        print(f"Checkout The Big Brain On {self.user['first_name']}!\n")
        print(f"You scored {score}%")
        print('***************************************************************')
        time.sleep(5)
        os.system('cls' if os.name == 'nt' else 'clear')


class User_prompt():
    quiz = Quiz()

    @classmethod
    def main(cls):
        
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'*** The Quiz Of All Quizes ***')
            welcome = input("Type Login/Register/Quit?\n").lower()
            if welcome =='login':
                if cls.quiz.login():
                    if cls.quiz.user['admin'] ==  True:
                        cls.quiz.admin()
                    else:
                        cls.quiz.guest()
            elif welcome == 'register'.lower():
                if cls.quiz.register():
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('You Have Successully Registered!')
                    continue
                else:
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print('Please Try Again...')
                    break
            elif welcome == 'quit':
                break 
            else:
                print("*** Invalid Option ***")

if __name__ == "__main__":
    User_prompt.main()
