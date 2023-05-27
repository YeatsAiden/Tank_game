import pygame
import random
import settings


def clip_img(surf, x, y, width, height):
        # It makes clips of all your FAILURES
        img_copy = surf.copy()
        clip_rect = pygame.Rect(x, y, width, height)
        img_copy.set_clip(clip_rect)
        return img_copy.subsurface(img_copy.get_clip())

class Font:
    def __init__(self, path, size):
        self.font_image = pygame.image.load(path).convert()
        self.spacing = 2
        self.size = size
        self.character_set = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '.', '-', ',', ':', '+', "'", '!', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '(', ')', '/', '_', '=', '\\', '[', ']', '*', '"', '<', '>', ';']
        self.character_index = 0
        self.charcter_width = 0
        self.characters = {}
        self.text_render = pygame.event.custom_type()
        pygame.time.set_timer(self.text_render, 100)
        self.speech_bubble_text_offset = self.calculate_offset()

        self.sentences = {}
        self.blip_1 = pygame.mixer.Sound("assets/sounds/blip_1.wav")
        self.blip_2 = pygame.mixer.Sound("assets/sounds/blip_2.wav")
        self.blip_3 = pygame.mixer.Sound("assets/sounds/blip_3.wav")
        self.blips = [self.blip_1, self.blip_2, self.blip_3]

        for x in range(self.font_image.get_width()):
            color = self.font_image.get_at((x, 0))
            if color == (0, 0, 255, 255):
                character_img = clip_img(self.font_image, x - self.charcter_width, 0, self.charcter_width, self.font_image.get_height())
                self.characters[self.character_set[self.character_index]] = pygame.transform.scale(character_img, (character_img.get_width() * size, character_img.get_height() * size))
                self.charcter_width = 0
                self.character_index += 1
            else:
                 self.charcter_width += 1
    

    def render_text(self, surf, text, x, y):
        # Will render text
        x_offset = 0
        y_offset = 0
        for index, letter in enumerate(text):
            if letter != ' ' and letter != "ඞ":
                character_img = self.characters[letter]
                character_img.set_colorkey((0, 0, 0))
                surf.blit(character_img, (x + x_offset , y + y_offset))
                x_offset += self.characters[letter].get_width() + self.spacing
            elif letter == ' ':
                x_offset += 5
            else:
                if index != 0:
                    x_offset = 0
                    y_offset += self.font_image.get_height() * self.size

         
    def create_speech_bubble(self, name, text, rect):
        # Creates a new speech_bubble process
        self.sentences[name] = {
            "words": [word for word in text.split()],
            "sentence": [],
            "word_index": 0,
            "letter_index": 0,
            "rect":rect,
            "done": False,
        }


    def render_dialogue(self, surf, name):
        # AAAAHHHHHHGHGHGHGHGHGHHGHGH my brain is fried and isn't capable of explaining this, try yourself, or if you are a prompt engineer and earn 25000$ a month from asking ChatGPT questions, then ask him :|
        # take note that settings.event is a global variable containing all events happening, put the events variable in a seperate file :\
        for event in settings.event:
            if event.type == self.text_render:
                if self.sentences[name]["word_index"] != len(self.sentences[name]["words"]) and not self.sentences[name]["done"]:
                    if self.sentences[name]["letter_index"] == 0:
                        self.sentences[name]["sentence"].append('')
                    if self.sentences[name]["letter_index"] != len(self.sentences[name]["words"][self.sentences[name]["word_index"]]):
                        self.sentences[name]["sentence"][len(self.sentences[name]["sentence"]) - 1] += self.sentences[name]["words"][self.sentences[name]["word_index"]][self.sentences[name]["letter_index"]]
                        self.sentences[name]["letter_index"] += 1
                        random.choice(self.blips).play()
                    else:
                        if self.check_if_sentence_is_to_long_for_speech_bubble(name, ''.join(self.sentences[name]["sentence"])):
                            self.sentences[name]["sentence"].insert(len(self.sentences[name]["sentence"]) - 1, "ඞ")
                        self.sentences[name]["sentence"].append(" ") 
                        self.sentences[name]["word_index"] += 1
                        self.sentences[name]["letter_index"] = 0
                else:
                    self.sentences[name]["done"] = True
        self.render_text(surf, ''.join(self.sentences[name]["sentence"]), self.sentences[name]["rect"].x + self.speech_bubble_text_offset[0], self.sentences[name]["rect"].y + self.speech_bubble_text_offset[1])
    

    def check_if_sentence_is_to_long_for_speech_bubble(self, name, str):
        # I make great function names "Don't you judge me Paul Blart, Pahud-scene", google it and watch it.
        width = 0
        str_array = str.split('ඞ')
        for line in str_array:
            for letter in line:
                if letter != ' ' and letter != 'ඞ':
                    character_img = self.characters[letter]
                    width += character_img.get_width() + self.spacing
                elif letter == ' ':
                    width += 5
            if width + self.speech_bubble_text_offset[0] > self.sentences[name]["rect"].width:
                return True
            else:
                width = 0
        return False


    def calculate_offset(self):
        # It just calculates where the text should start in the speech bubble
        return [self.font_image.get_width() / len(self.character_set) * self.size, self.font_image.get_height() * self.size]
        
