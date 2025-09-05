import pygame
import random
import string
from morse_utils import encode_to_morse
from audio import play_morse

EXIT_COMMAND = "/quit"

def practice_mode(unit_s, num_chars=5):
    chars = string.ascii_uppercase + string.digits
    print(f"\nPractice Mode: Type back the {num_chars} characters you hear in Morse.")
    print("Press ESC to repeat Morse, TAB to advance, or close the window to exit.\n")

    screen = pygame.display.set_mode((500, 100))
    pygame.display.set_caption("Morse Practice (ESC=repeat, TAB=next)")

    font = pygame.font.Font(None, 36)

    running = True
    while running:
        seq = ''.join(random.choice(chars) for _ in range(num_chars))
        morse = encode_to_morse(seq)
        answered = False
        user_input = ""

        play_morse(morse, unit_s)
        feedback = ""
        while not answered and running:
            screen.fill((30, 30, 30))
            prompt = f"Type answer ({num_chars} chars): {user_input}"
            text = font.render(prompt, True, (200, 200, 200))
            screen.blit(text, (20, 40))
            if feedback:
                feedback_text = font.render(feedback, True, (255, 180, 180))
                screen.blit(feedback_text, (20, 70))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    answered = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        play_morse(morse, unit_s)
                    elif event.key == pygame.K_F2:
                        if feedback:
                            print(feedback)
                        answered = True
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input.upper() == EXIT_COMMAND.upper():
                            running = False
                            answered = True
                        elif user_input:
                            if user_input.upper() == seq:
                                feedback = "Correct!"
                            else:
                                feedback = f"Incorrect. The answer was: {seq}"
                            user_input = ""
                    else:
                        char = event.unicode.upper()
                        if char in chars and len(user_input) < num_chars:
                            user_input += char
            pygame.time.wait(10)