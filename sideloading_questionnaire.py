#!/usr/bin/env python3
"""
Sideloading Questionnaire System
A script for conducting the 600-question personality modeling questionnaire.
Follows the principles from AGENTS.md for clean, readable, and maintainable code.
"""

import os
import sys
from typing import List, Dict, Tuple, Optional


class QuestionnaireManager:
    """Manages the questionnaire session including loading questions and saving answers."""
    
    AVAILABLE_LANGUAGES = {
        'spanish': 'español',
        'english': 'ingles',  # If available
        'german': 'aleman',
        'chinese': 'chino',
        'french': 'frances',
        'greek': 'griego',
        'hungarian': 'hungaro',
        'italian': 'italiano',
        'japanese': 'japones',
        'polish': 'polaco',
        'portuguese': 'portugues',
        'russian': 'ruso'
    }
    
    def __init__(self):
        self.current_language = None
        self.questions = []
        self.answers_file_path = None
        self.questions_file_path = None
    
    def display_welcome_message(self) -> None:
        """Display welcome message in English."""
        print("=" * 60)
        print("🎯 WELCOME TO THE SIDELOADING QUESTIONNAIRE SYSTEM 🎯")
        print("=" * 60)
        print("\nThis system will guide you through a comprehensive")
        print("600-question personality modeling questionnaire.")
        print("\nYou can stop at any time and resume later where you left off.")
        print("Your progress will be automatically saved.")
        print("=" * 60)
    
    def display_available_languages(self) -> None:
        """Display available languages for the questionnaire."""
        print("\n📋 AVAILABLE LANGUAGES:")
        print("-" * 30)
        for idx, (english_name, file_suffix) in enumerate(self.AVAILABLE_LANGUAGES.items(), 1):
            # Check if the file actually exists
            file_path = f"600Q_{file_suffix}.txt"
            if os.path.exists(file_path):
                print(f"{idx:2d}. {english_name.title()}")
        print("-" * 30)
    
    def get_language_choice(self) -> str:
        """Get user's language choice and return the file suffix."""
        while True:
            self.display_available_languages()
            try:
                choice = input("\nPlease enter the number of your preferred language: ").strip()
                choice_num = int(choice)
                
                available_langs = list(self.AVAILABLE_LANGUAGES.items())
                if 1 <= choice_num <= len(available_langs):
                    english_name, file_suffix = available_langs[choice_num - 1]
                    
                    # Verify file exists
                    if os.path.exists(f"600Q_{file_suffix}.txt"):
                        self.current_language = file_suffix
                        print(f"\n✅ Great! You selected: {english_name.title()}")
                        return file_suffix
                    else:
                        print(f"\n❌ Sorry, the {english_name} questionnaire file is not available.")
                        continue
                else:
                    print("\n❌ Invalid choice. Please select a valid number.")
            except ValueError:
                print("\n❌ Please enter a valid number.")
    
    def load_questions(self, language_suffix: str) -> bool:
        """Load questions from the specified language file."""
        self.questions_file_path = f"600Q_{language_suffix}.txt"
        
        if not os.path.exists(self.questions_file_path):
            print(f"❌ Questions file not found: {self.questions_file_path}")
            return False
        
        try:
            with open(self.questions_file_path, 'r', encoding='utf-8') as file:
                self.questions = [line.strip() for line in file if line.strip()]
            
            print(f"✅ Loaded {len(self.questions)} questions successfully!")
            return True
        except Exception as e:
            print(f"❌ Error loading questions: {e}")
            return False
    
    def get_last_answered_question(self) -> int:
        """Check answers file and return the ID of the last answered question."""
        if not os.path.exists(self.answers_file_path):
            return 0
        
        try:
            with open(self.answers_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Find the last valid answer entry
            last_id = 0
            for line in lines:
                line = line.strip()
                if line and ';' in line:
                    try:
                        parts = line.split(';', 2)  # Split into max 3 parts
                        if len(parts) >= 3:
                            question_id = int(parts[0])
                            last_id = max(last_id, question_id)
                    except ValueError:
                        continue
            
            return last_id
        except Exception as e:
            print(f"⚠️  Warning: Could not read answers file: {e}")
            return 0
    
    def save_answer(self, question_id: int, question: str, answer: str) -> None:
        """Save a single answer to the answers file."""
        try:
            with open(self.answers_file_path, 'a', encoding='utf-8') as file:
                # Format: ID;Question;Answer
                file.write(f"{question_id};{question};{answer}\n")
        except Exception as e:
            print(f"❌ Error saving answer: {e}")
    
    def start_questionnaire_session(self) -> None:
        """Start or resume the questionnaire session."""
        if not self.questions:
            print("❌ No questions loaded. Please restart the program.")
            return
        
        self.answers_file_path = f"600A_{self.current_language}.txt"
        
        # Check for existing progress
        last_answered = self.get_last_answered_question()
        start_question = last_answered
        
        if last_answered > 0:
            print(f"\n🔄 RESUMING SESSION")
            print(f"You have already answered {last_answered} questions.")
            print(f"Starting from question {last_answered + 1}...")
        else:
            print(f"\n🆕 STARTING NEW SESSION")
            print(f"Beginning with question 1 of {len(self.questions)}...")
        
        print(f"💾 Answers will be saved to: {self.answers_file_path}")
        print("\n" + "=" * 60)
        print("📝 QUESTIONNAIRE INSTRUCTIONS:")
        print("• Answer each question as detailed as possible")
        print("• Type 'QUIT' at any time to save and exit")
        print("• Type 'SKIP' to skip a question")
        print("• Your progress is automatically saved")
        print("=" * 60)
        
        input("\nPress ENTER to continue...")
        
        # Start asking questions
        for i in range(start_question, len(self.questions)):
            if not self.ask_question(i):
                break
        
        if start_question < len(self.questions):
            print(f"\n🎉 QUESTIONNAIRE COMPLETED!")
            print(f"All {len(self.questions)} questions have been answered.")
            print(f"Your complete responses are saved in: {self.answers_file_path}")
        
    def ask_question(self, question_index: int) -> bool:
        """Ask a single question and save the answer. Returns False if user wants to quit."""
        question_id = question_index
        question_text = self.questions[question_index]
        
        # Remove the number prefix if it exists (e.g., "1. " -> "")
        if '. ' in question_text and question_text.split('. ', 1)[0].isdigit():
            question_text = question_text.split('. ', 1)[1]
        
        print(f"\n" + "-" * 60)
        print(f"Question {question_id + 1} of {len(self.questions)}")
        print("-" * 60)
        print(f"📋 {question_text}")
        print("-" * 60)
        
        while True:
            try:
                answer = input("Your answer: ").strip()
                
                if answer.upper() == 'QUIT':
                    print(f"\n💾 Session saved! You can resume from question {question_id + 1} next time.")
                    return False
                elif answer.upper() == 'SKIP':
                    answer = "[SKIPPED]"
                elif not answer:
                    print("Please provide an answer, type 'SKIP' to skip, or 'QUIT' to exit.")
                    continue
                
                # Save the answer
                self.save_answer(question_id, self.questions[question_index], answer)
                print("💾 Answer saved!")
                return True
                
            except KeyboardInterrupt:
                print(f"\n\n💾 Session interrupted! Progress saved. Resume from question {question_id + 1} next time.")
                return False
            except Exception as e:
                print(f"❌ Error: {e}. Please try again.")


def main():
    """Main function to run the questionnaire system."""
    try:
        manager = QuestionnaireManager()
        
        # Display welcome and get language choice
        manager.display_welcome_message()
        language_suffix = manager.get_language_choice()
        
        # Load questions for the selected language
        if not manager.load_questions(language_suffix):
            print("❌ Failed to load questions. Exiting.")
            sys.exit(1)
        
        # Start the questionnaire session
        manager.start_questionnaire_session()
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Your progress has been saved.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 