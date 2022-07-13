import os
import sqlite3

# TODO: TESTING

import pygame
from pygame import mixer
import math

from Assets import *
from Colours import *
from Strings_English import *


# TODO: Simplify Code
#  Create Text Box With Multiple Lines
#  METRE RECT ATTRIBUTE
#  Pass Game Variable instead of using global constant??

# TODO: PARAGRAPH
# TODO: PAGE CLASSES
# TODO: THE VIEW ELEMENTS SHOULD MOVE IF THEIR PARENT IS MOVED OR CHANGES IN SIZE, ATTRIBUTES FOR WHETHER THIS HAPPENS

# TODO: DEBUG FILE


class Game:
    DEFAULT_FRAME_RATE = 60

    def __init__(self):

        pygame.init()
        mixer.init()

        self.done = False
        self.database_helper = DatabaseHelper()

        # Game may be stretched to fit aspect ratios.
        # The player views a cross-section of the game world.
        # Different aspect ratios could mean that the player cannot see objects in the game world that they should be
        # able to see, or see objects that they shouldn't.
        # Many 2D games purposefully lock the aspect ratio for this reason.

        # The game window corresponds to 16m horizontal, 9m vertical.
        # All measurements, except for rect, are worked with as metres, then converted to pixels when needed.
        self.window_dimensions = [16, 9]

        # Getting the resolution of the physical screen:
        screen_info = pygame.display.Info()
        self.resolution = [screen_info.current_w, screen_info.current_h]

        # If the user has chosen a specific frame rate cap, using that. Otherwise, using 60:
        frame_rate = self.database_helper.get_frame_rate()
        if frame_rate is not None:
            self.frame_rate = frame_rate
        else:
            self.frame_rate = self.DEFAULT_FRAME_RATE
            self.database_helper.set_frame_rate(self.frame_rate)

        # If the user has chosen an FPS counter setting, using that. Otherwise, using OFF:
        show_frame_rate = self.database_helper.get_show_frame_rate()
        if show_frame_rate is not None:
            self.show_frame_rate = show_frame_rate
        else:
            self.show_frame_rate = False
            self.database_helper.set_show_frame_rate(False)

        volume = self.database_helper.get_volume()
        if volume is not None:
            self.audio_volume = volume
        else:
            self.audio_volume = 1
            self.database_helper.set_volume(1)

        self.frame_time = 1 / self.frame_rate

        self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        self.rect = self.screen.get_rect()

        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()

        self.font = FONT

        self.settings_page = None

        self.all_events = []
        self.key_down_events = []

    def start(self):
        self.set_up_pages()
        self.show_main_menu()

    def update(self):
        # If the user has enabled the FPS counter, displaying it:
        if self.show_frame_rate:
            fps_text = Text(str(int(self.clock.get_fps())), location=[0.5, 0.5], font_size=0.5)
            fps_text.draw()

    def is_done(self):
        return self.done

    def set_up_pages(self):
        # Instantiating classes for the necessary pages:
        self.settings_page = SettingsPage()

    def quit(self):
        self.done = True

    def get_screen(self):
        return self.screen

    def get_clock(self):
        return self.clock

    def get_rect(self):
        return self.rect

    def get_frame_rate(self):
        return self.frame_rate

    def set_frame_rate(self, frame_rate):
        self.frame_rate = frame_rate
        self.frame_time = 1 / frame_rate
        self.database_helper.set_frame_rate(frame_rate)

    def get_frame_time(self):
        return self.frame_time

    def set_frame_time(self, frame_time):
        self.frame_time = frame_time
        self.frame_rate = 1 / frame_time

    def get_show_frame_rate(self):
        return self.show_frame_rate

    def set_show_frame_rate(self, value):
        self.show_frame_rate = value
        self.database_helper.set_show_frame_rate(value)

    def get_audio_volume(self):
        return self.audio_volume

    def set_audio_volume(self, volume):
        self.audio_volume = volume
        self.database_helper.set_volume(volume)

    def get_font(self, size):
        # The size of the font is in metres.
        return pygame.font.SysFont(self.font, int(size * (self.resolution[0] / self.window_dimensions[0])))

    #  ALWAYS STORE PIXEL COUNTERPARTS SINCE FOR EACH MEASUREMENT, IT IS CALCULATED MANY TIMES?  YES BUT DO THIS LATER!!
    def metre_to_pixel(self, value):
        return int(value * (self.resolution[0] / self.window_dimensions[0]))

    def metre_to_pixel_point(self, values):
        return int(values[0] * (self.resolution[0] / self.window_dimensions[0])), \
               int(values[1] * (self.resolution[1] / self.window_dimensions[1]))

    def pixel_to_metre(self, value):
        return value / (self.resolution[0] / self.window_dimensions[0])

    def pixel_to_metre_point(self, values):
        return values[0] / (self.resolution[0] / self.window_dimensions[0]), \
               values[1] / (self.resolution[0] / self.window_dimensions[0])

    def get_key_down_events(self):
        return self.key_down_events

    def get_inputs(self):
        self.all_events = pygame.event.get()
        self.key_down_events = []

        for event in self.all_events:
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                self.key_down_events.append(event.key)

    def key_pressed(self, key_id):
        for key_input in self.key_down_events:
            if key_input == key_id: return True
        return False

    # TODO: SAME LOOP BEING ENTERED FOR MANY THINGS, MAKE THESE ATTRIBUTES INSTEAD? JUST SEARCH FOR pygame.MOUSEBUTTONDOWN in self.all_events BUT DO IT LATER!!!! BUT IS THIS JUST AS INEFFICIENT
    def mouse_pressed(self):
        for event in self.all_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return True
        return False

    def mouse_released(self):
        for event in self.all_events:
            if event.type == pygame.MOUSEBUTTONUP:
                return True
        return False

    def show_pause_menu(self):

        view_group = []

        btn_menu = Button(RETURN_TO_MENU, location=self.pixel_to_metre_point(self.rect.center))
        view_group.append(btn_menu)

        btn_help = Button(SHOW_HELP, below=btn_menu)
        view_group.append(btn_help)

        btn_resume = Button(RESUME_GAME, above=btn_menu)
        view_group.append(btn_resume)

        btn_quit = Button(QUIT, below=btn_help)
        view_group.append(btn_quit)

        txt_paused = Text(PAUSED, frame_condition=1)
        txt_paused.centre_between(self.rect.topleft, self.pixel_to_metre_point(btn_resume.get_rect().topleft))
        txt_paused.set_italic(True)
        view_group.append(txt_paused)

        while not self.done:
            self.get_inputs()
            if self.key_pressed(pygame.K_ESCAPE): return

            self.screen.fill(WHITE)

            for view in view_group: view.draw()

            # On Click:
            if btn_resume.clicked():
                return
            elif btn_help.clicked():
                self.show_help()
            elif btn_menu.clicked():
                self.show_main_menu()
            elif btn_quit.clicked():
                self.quit()

            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def show_main_menu(self):
        frame = 1

        view_group = []

        btn_start = Button(PLAY_GAME, location=self.pixel_to_metre_point(self.rect.center))
        view_group.append(btn_start)

        btn_settings = Button(SETTINGS, below=btn_start)
        view_group.append(btn_settings)

        btn_quit = Button(QUIT, below=btn_settings)
        view_group.append(btn_quit)

        title = Text(GAME_NAME,
                     frame_condition=1,
                     frame_thickness=0.04,
                     padding=0.5,
                     font_size=1.75)
        title.centre_between(GAME.pixel_to_metre_point(self.rect.midtop),
                             GAME.pixel_to_metre_point(btn_start.get_rect().midtop))
        title.set_italic(True)
        view_group.append(title)

        while not self.done:
            self.get_inputs()
            if self.key_pressed(pygame.K_SPACE):
                self.show_game()
                return
            elif self.key_pressed(pygame.K_1):
                self.button_showcase()

            self.screen.fill(WHITE)

            for view in view_group: view.draw()

            # On Click:
            if btn_start.clicked():
                self.show_game()
                return
            elif btn_settings.clicked():
                self.settings_page.show()
            elif btn_quit.clicked():
                self.quit()

            placeholder = self.get_font(0.5).render(str(frame), True, BLACK)
            self.screen.blit(placeholder, self.metre_to_pixel_point([15, 0.5]))

            frame += 1
            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def show_help(self):

        while not self.done:
            self.get_inputs()
            if self.key_pressed(pygame.K_ESCAPE): return

            self.screen.fill(WHITE)
            placeholder = self.get_font(1).render("Help Menu", False, BLUE)
            self.screen.blit(placeholder, self.metre_to_pixel_point([1, 1]))

            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def show_game(self):

        frame = 1
        while not self.done:
            self.get_inputs()

            # The key bindings depend on which page the user is at.
            # For example, the user should not be able to open their inventory before selecting a player.
            # For this reason, keys are bound on a per-method basis, 
            if self.key_pressed(pygame.K_ESCAPE):
                self.show_pause_menu()
            elif self.key_pressed(pygame.K_TAB):
                self.show_map()
            elif self.key_pressed(pygame.K_h):
                self.show_help()
            elif self.key_pressed(pygame.K_e):
                self.show_inventory()

            self.screen.fill(WHITE)
            placeholder = self.get_font(1).render("Game", True, BLACK)
            self.screen.blit(placeholder, self.metre_to_pixel_point([1, 1]))

            placeholder = self.get_font(0.5).render(str(frame), True, BLACK)
            self.screen.blit(placeholder, self.metre_to_pixel_point([15, 0.5]))

            frame += 1
            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def show_inventory(self):

        while not self.done:
            self.get_inputs()
            if self.key_pressed(pygame.K_ESCAPE): return

            self.screen.fill(WHITE)
            placeholder = self.get_font(1).render("Inventory Menu", False, YELLOW)
            self.screen.blit(placeholder, [1, 1])

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def show_map(self):

        while not self.done:
            self.get_inputs()
            if self.key_pressed(pygame.K_ESCAPE): return

            self.screen.fill(WHITE)
            placeholder = self.get_font(1).render("Map Menu", False, CYAN)
            self.screen.blit(placeholder, self.metre_to_pixel_point([1, 1]))

            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def button_showcase(self):
        view_group = []

        # The appearance of a default button:
        btn_1 = Button("Button 1", location=[1.75, 0.75])
        view_group.append(btn_1)

        btn_2 = Button("Button 2",
                       to_right_of=btn_1,
                       frame_condition=Text.ALWAYS,
                       frame_thickness=0,
                       padding=1,
                       font_size=0.3,
                       corner_radius=0,
                       frame_colour=RED,
                       text_colour=BLUE,
                       hover_frame_colour=YELLOW,
                       hover_text_colour=BLUE
                       )
        view_group.append(btn_2)

        btn_3 = Button("Button 3",
                       frame_thickness=0.1,
                       to_right_of=btn_2,
                       font_size=0.5,
                       corner_radius=0.1,
                       frame_colour=GREY,
                       text_colour=MAROON,
                       hover_frame_colour=PLATINUM
                       )
        view_group.append(btn_3)

        btn_4 = Button("Button 4",
                       to_right_of=btn_3,
                       frame_condition=Text.ALWAYS,
                       frame_thickness=0,
                       font_size=0.8,
                       corner_radius=1,
                       frame_colour=MAGENTA,
                       text_colour=CYAN,
                       hover_frame_colour=CYAN,
                       hover_text_colour=MAGENTA
                       )
        view_group.append(btn_4)

        btn_5 = Button("Button 5",
                       to_right_of=btn_4,
                       frame_condition=Text.NEVER,
                       margin=1,
                       font_size=1,
                       )
        view_group.append(btn_5)

        btn_6 = Button("B6",
                       below=btn_5,
                       frame_condition=Text.ALWAYS,
                       padding=1,
                       corner_radius=2,
                       font_size=0.4,
                       hover_frame_colour=GREEN,
                       hover_text_colour=GREEN
                       )

        view_group.append(btn_6)

        btn_7 = Button("Button 7",
                       to_left_of=btn_6,
                       frame_condition=Text.ALWAYS,
                       frame_thickness=0,
                       margin=1,
                       padding=0.1,
                       text_colour=SMOKE,
                       frame_colour=MAROON,
                       hover_text_colour=PLATINUM,
                       hover_frame_colour=MAROON
                       )
        view_group.append(btn_7)

        edt_txt_1 = EditText(hint="INPUT HINT", max_length=10, below=btn_7, margin=1)
        view_group.append(edt_txt_1)

        txt_pointer = Text("Input Field >>>", to_left_of=edt_txt_1)
        view_group.append(txt_pointer)

        edt_txt_2 = EditText(hint="INPUT HERE WILL BECOME HINT", clear_on_focus=True, max_length=15,
                             below=edt_txt_1, margin=0.25, font_size=0.5)
        view_group.append(edt_txt_2)

        sl_1 = Slider(bar_size=[1, 1], start_value=[0.5, 0.5], below=edt_txt_2,
                      slide_horizontal=True,
                      slide_vertical=True, margin=1, padding=0)
        view_group.append(sl_1)

        img_health = ImageButton(MEDKIT, to_right_of=sl_1, frame_condition=Button.NEVER, margin=0.1, padding=0)
        view_group.append(img_health)

        # img_speed = ImageButton()

        txt_slider_value = Text("", to_left_of=sl_1, margin=1, frame_condition=Text.ALWAYS, font_size=0.5, padding=0.25)
        view_group.append(txt_slider_value)

        sl_2 = Slider(to_left_of=txt_slider_value, margin=1)
        view_group.append(sl_2)

        while not self.done:
            self.get_inputs()
            if self.key_pressed(pygame.K_ESCAPE): return

            self.screen.fill(WHITE)
            txt_slider_value.set_text_string([round(item, 2) for item in sl_1.get_value()])
            for view in view_group:
                view.draw()

            pygame.display.flip()
            self.clock.tick(self.frame_rate)


class SettingsPage:

    def __init__(self):
        # Declaring required View objects and page layout:

        self.views = []

        # Show Frame Rate Selector:
        print(GAME.get_show_frame_rate())

        if GAME.get_show_frame_rate():
            start_index = 1
        else:
            start_index = 0

        self.sel_frame_rate = Selector(start_index=start_index,
                                       location=GAME.pixel_to_metre_point(GAME.get_rect().center),
                                       font_size=0.5)
        self.views.append(self.sel_frame_rate)

        # Show Frame Rate Text:
        self.txt_show_frame_rate = Text(SHOW_FRAME_RATE,
                                        to_left_of=self.sel_frame_rate,
                                        font_size=0.5)
        self.views.append(self.txt_show_frame_rate)

        # Max Frame Rate Input:
        self.edt_txt_frame_rate = EditText(hint=str(GAME.get_frame_rate()),
                                           clear_on_focus=True,
                                           input_type=EditText.INTEGER,
                                           max_length=3,
                                           above=self.sel_frame_rate,
                                           font_size=0.5)
        self.views.append(self.edt_txt_frame_rate)

        # Frame Rate Text:
        self.txt_frame_rate = Text(FRAME_RATE_LIMIT,
                                   to_left_of=self.edt_txt_frame_rate,
                                   font_size=0.5)
        self.views.append(self.txt_frame_rate)

        # Resolution Value Text:
        self.txt_resolution_value = Text(RESOLUTION_FORMAT.format(*GAME.resolution),
                                         above=self.edt_txt_frame_rate,
                                         frame_condition=Text.ALWAYS,
                                         font_size=0.5)
        self.views.append(self.txt_resolution_value)

        # Resolution Text:
        self.txt_resolution = Text(RESOLUTION,
                                   to_left_of=self.txt_resolution_value,
                                   font_size=0.5)
        self.views.append(self.txt_resolution)

        # Audio Volume Slider
        self.sl_volume = Slider(below=self.sel_frame_rate,
                                start_value=[GAME.get_audio_volume(), 0])
        self.views.append(self.sl_volume)

        # Audio Volume Text
        self.txt_volume = Text(AUDIO_VOLUME,
                               to_left_of=self.sl_volume,
                               font_size=0.5)
        self.views.append(self.txt_volume)

        # Settings Text:
        self.txt_settings = Text(SETTINGS)
        self.txt_settings.centre_between(GAME.pixel_to_metre_point(GAME.get_rect().midtop),
                                         GAME.pixel_to_metre_point(self.txt_resolution_value.get_rect().midtop))
        self.views.append(self.txt_settings)

        # Save & Exit Button
        self.btn_exit = Button(BACK,
                               font_size=0.5)
        self.btn_exit.centre_between(GAME.pixel_to_metre_point(self.sel_frame_rate.get_rect().midbottom),
                                     GAME.pixel_to_metre_point(GAME.get_rect().midbottom))
        self.views.append(self.btn_exit)

    def show(self):
        mixer.music.load(MAIN_MENU_MUSIC)
        mixer.music.set_volume(GAME.get_audio_volume())
        mixer.music.play(-1)

        while not GAME.is_done():
            GAME.get_inputs()

            # Drawing all view objects:
            GAME.get_screen().fill(WHITE)

            # If the refresh rate has been changed and the input is not empty, set it to the attribute:
            if self.edt_txt_frame_rate.unfocused() and not self.edt_txt_frame_rate.input_empty():
                frame_rate = int(self.edt_txt_frame_rate.get_text_string())
                GAME.set_frame_rate(frame_rate)

            # Changing the frame rate display if the frame rate selector is clicked:
            if self.sel_frame_rate.clicked():
                GAME.set_show_frame_rate(self.sel_frame_rate.get_state() == ON)

            # If the audio volume slider has been changed:
            if self.sl_volume.handle_released():
                GAME.set_audio_volume(self.sl_volume.get_value()[0])
                mixer.music.set_volume(self.sl_volume.get_value()[0])

            # Exit if exit button or escape clicked:
            if self.btn_exit.clicked() or GAME.key_pressed(pygame.K_ESCAPE):
                mixer.music.stop()
                return




            for view in self.views: view.draw()

            GAME.update()
            pygame.display.flip()
            GAME.get_clock().tick(GAME.get_frame_rate())


class View(pygame.sprite.Sprite):

    def __init__(self, size=None, location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5):

        super().__init__()

        self.location = location

        self.rect = None

        self.margin = margin
        self.padding = padding

        if size is not None:
            self.set_size(size)
        else:
            self.size = None

        self.above = above
        self.below = below
        self.to_right_of = to_right_of
        self.to_left_of = to_left_of

        self.calculate_location()

    def calculate_location(self):
        # TODO: CASCADING

        # If a location is not explicitly stated, it is calculated according to the new View's relation to the old one:
        # The margin is the distance between the two Views.
        if self.above is not None:
            self.location = [self.above.get_location()[0],
                             self.above.get_location()[1] - 0.5 * self.size[1] - 0.5 * self.above.get_size()[
                                 1] - self.margin]

        elif self.below is not None:
            self.location = [self.below.get_location()[0],
                             self.below.get_location()[1] + 0.5 * self.size[1] + 0.5 * self.below.get_size()[
                                 1] + self.margin]

        elif self.to_left_of is not None:
            self.location = [
                self.to_left_of.get_location()[0] - 0.5 * self.size[0] - 0.5 * self.to_left_of.get_size()[
                    0] - self.margin,
                self.to_left_of.get_location()[1]]

        elif self.to_right_of is not None:
            self.location = [
                self.to_right_of.get_location()[0] + 0.5 * self.size[0] + 0.5 * self.to_right_of.get_size()[
                    0] + self.margin,
                self.to_right_of.get_location()[1]]

    def centre_between(self, location_1, location_2):
        # Sets the location of the View between 2 points:
        self.location = (location_1[0] + location_2[0]) / 2, (location_1[1] + location_2[1]) / 2

    def get_location(self):
        return self.location

    def get_rect(self):
        return self.rect

    def set_size(self, size):
        self.size = [item + self.padding for item in size]

    def get_size(self):
        return self.size


class Text(View):
    NEVER = 0
    ALWAYS = 1

    def __init__(self, text_string, size=None,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5,
                 frame_condition=0, frame_thickness=0.05, corner_radius=0.1,
                 font_size=0.8, frame_colour=BLACK, text_colour=BLACK):

        # Determines when the frame (border or background) of the button instance should be displayed.
        self.frame_condition = frame_condition

        self.font_size = font_size
        self.font = GAME.get_font(self.font_size)
        self.text_string = str(text_string)
        self.text = self.font.render(self.text_string, True, text_colour)

        self.frame_colour = frame_colour
        self.text_colour = text_colour

        self.thickness = frame_thickness
        self.corner_radius = corner_radius

        self.frame = None
        frame_size = GAME.pixel_to_metre_point(self.text.get_size())

        super().__init__(size=frame_size, location=location, above=above, below=below, to_right_of=to_right_of,
                         to_left_of=to_left_of,
                         margin=margin, padding=padding)

        if self.location is not None: self.calculate_frame()

    def centre_between(self, location_1, location_2):
        super().centre_between(location_1, location_2)
        self.calculate_frame()

    def get_text_string(self):
        return self.text_string

    def set_text_string(self, text_string):
        self.text_string = text_string
        self.text = self.font.render(str(self.text_string), True, self.text_colour)
        self.set_size(GAME.pixel_to_metre_point(self.text.get_size()))
        self.calculate_frame()

    def calculate_frame(self):
        self.rect = self.text.get_rect(center=(GAME.metre_to_pixel_point(self.location)))
        # Tentative location value [0,0], corrected afterwards:
        self.frame = pygame.Rect([0, 0], GAME.metre_to_pixel_point(self.size))
        self.frame.center = GAME.metre_to_pixel_point(self.location)

    def draw(self):
        if self.frame_condition == self.ALWAYS: self.draw_frame(self.frame_colour)
        self.draw_text(self.text_colour)

    def draw_frame(self, colour):
        pygame.draw.rect(GAME.get_screen(), colour, self.frame, GAME.metre_to_pixel(self.thickness),
                         GAME.metre_to_pixel(self.corner_radius))

    def draw_text(self, colour):
        GAME.get_screen().blit(self.font.render(str(self.text_string), True, colour), self.rect)

    def set_text_color(self, text_colour):
        self.text = GAME.get_font(self.font_size).render(self.text_string, True, text_colour)

    def set_italic(self, value):
        self.font.set_italic(value)
        self.text = self.font.render(self.text_string, True, self.text_colour)
        self.calculate_frame()

    def set_bold(self, value):
        self.font.set_bold(value)
        self.text = self.font.render(self.text_string, True, self.text_colour)
        self.calculate_frame()

    def set_underline(self, value):
        self.font.set_underline(value)
        self.text = self.font.render(self.text_string, True, self.text_colour)
        self.calculate_frame()


class Button(Text):
    HOVER = 2

    # TODO: Is there a way to copy arguments? Need to write one by one?
    def __init__(self, text_string,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5,
                 frame_condition=2, frame_thickness=0.05, corner_radius=0.1,
                 font_size=0.8, frame_colour=BLACK, text_colour=BLACK,
                 hover_frame_colour=SMOKE, hover_text_colour=BLACK):

        super().__init__(
            text_string, location=location, above=above, below=below, to_right_of=to_right_of, to_left_of=to_left_of,
            margin=margin, padding=padding, corner_radius=corner_radius,
            frame_condition=frame_condition, frame_thickness=frame_thickness,
            font_size=font_size, frame_colour=frame_colour, text_colour=text_colour)

        # The colours when the mouse cursor is on top of the Button:
        self.hover_text_colour = hover_text_colour
        self.hover_frame_colour = hover_frame_colour

    def draw(self):
        # Determining correct colours to use and what to draw:
        if self.hovering():
            text_colour = self.hover_text_colour
            if self.frame_condition == self.ALWAYS or self.frame_condition == self.HOVER:
                self.draw_frame(self.hover_frame_colour)
        else:
            text_colour = self.text_colour
            if self.frame_condition == self.ALWAYS: self.draw_frame(self.frame_colour)

        self.draw_text(text_colour)

    def hovering(self):
        return self.frame.collidepoint(pygame.mouse.get_pos())

    def clicked(self):
        return self.hovering() and GAME.mouse_released()


class ImageButton(Button):

    def __init__(self, image, size=(0.5, 0.5),
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5,
                 frame_condition=Button.NEVER, frame_thickness=0.05, corner_radius=0.1,
                 font_size=0.8, frame_colour=BLACK, text_colour=BLACK,
                 hover_frame_colour=SMOKE):
        self.image = pygame.transform.scale(image, GAME.metre_to_pixel_point(size))
        self.image_size = size

        super().__init__("",
                         location=location, above=above, below=below, to_right_of=to_right_of, to_left_of=to_left_of,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         font_size=font_size, frame_colour=frame_colour, text_colour=text_colour,
                         hover_frame_colour=hover_frame_colour)

        # TODO: CAN WE SET IT CORRECTLY FIRST TIME?
        # Correcting size which was set according to the text:
        self.set_size(self.image_size)
        self.calculate_location()
        self.calculate_frame()

    def calculate_frame(self):
        # Overriding since frame must be drawn according to the image:
        self.rect = self.image.get_rect(center=(GAME.metre_to_pixel_point(self.location)))
        # Tentative location value [0,0], corrected afterwards:
        self.frame = pygame.Rect([0, 0], GAME.metre_to_pixel_point(self.size))
        self.frame.center = GAME.metre_to_pixel_point(self.location)

    def draw_image(self):
        GAME.get_screen().blit(self.image, self.rect.topleft)

    def draw(self):
        self.draw_image()

        super().draw()


class Selector(Button):

    def __init__(self, selection_strings=(OFF, ON), start_index=0,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5,
                 frame_condition=2, frame_thickness=0.05, corner_radius=0.1,
                 font_size=0.8, frame_colour=BLACK, text_colour=BLACK,
                 hover_frame_colour=SMOKE, hover_text_colour=BLACK):

        # This attribute is necessary. Otherwise, when getting the state if slider is clicked,
        # we get what the state was, not what it becomes after click:
        self.incremented = False

        self.selection_strings = [str(item) for item in selection_strings]
        self.selection_index = start_index

        super().__init__(self.selection_strings[self.selection_index],
                         location=location, above=above, below=below, to_right_of=to_right_of, to_left_of=to_left_of,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         font_size=font_size, frame_colour=frame_colour, text_colour=text_colour,
                         hover_frame_colour=hover_frame_colour, hover_text_colour=hover_text_colour)

    def draw(self):
        # Need to get state to see if a change in state is needed:
        self.set_text_string(self.get_state())
        self.calculate_frame()
        super().draw()

    def get_state(self):
        # If we did not update the state here, when we try to get the state after the selector has been clicked,
        # because the selector would not have been drawn, we would get what value it was before the click,
        # not after the click.

        if super().clicked():

            if not self.incremented:

                if self.selection_index < len(self.selection_strings) - 1:
                    self.selection_index += 1
                else:
                    self.selection_index = 0

                self.incremented = True

        else:
            self.incremented = False



        return self.selection_strings[self.selection_index]


class EditText(Button):
    STRING = 0
    INTEGER = 1
    FLOAT = 2

    def __init__(self, text_string=None, max_length=50, hint=PLACEHOLDER, clear_on_focus=False, input_type=0,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5,
                 frame_condition=1, frame_thickness=0.05, corner_radius=0.1,
                 font_size=0.8, frame_colour=BLACK, text_colour=BLACK,
                 hover_frame_colour=SMOKE, hover_text_colour=BLACK,
                 focus_frame_colour=IRIS, focus_text_colour=IRIS):

        # The type of input that is allowed:
        self.input_type = input_type

        # The hint is displayed if the TextEdit is empty.
        self.hint = hint

        # The maximum length the text can be:
        self.max_length = max_length

        # Whether to set input as hint and clear input field when unfocused.
        # Means that there is no need to delete previous input when entering new input.
        self.clear_on_focus = clear_on_focus

        if text_string is None:
            text_string = hint
            # Whether the hint is currently being shown:
            self.hint_active = True
        else:
            self.hint_active = False

        super().__init__(
            text_string, location=location, above=above, below=below, to_right_of=to_right_of, to_left_of=to_left_of,
            margin=margin, padding=padding,
            frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
            font_size=font_size, frame_colour=frame_colour, text_colour=text_colour,
            hover_frame_colour=hover_frame_colour, hover_text_colour=hover_text_colour)

        # The colours when the EditText is 'in focus'
        # (i.e. when it has been clicked and ready to edit):
        self.focus_frame_colour = focus_frame_colour
        self.focus_text_colour = focus_text_colour

        self.focused = False

    def draw(self):

        text_colour = self.text_colour

        # If the EditText has just been unfocused, set the text_string as hint and clear the input field
        # such that it is empty when focused again:
        if self.focused and self.unfocused() and self.clear_on_focus and self.text_string != "":
            self.set_hint(self.text_string)
            self.set_text_string("")

        if self.clicked():
            self.focused = True
        elif self.unfocused():
            self.focused = False

        if self.focused:
            text_colour = self.focus_text_colour
            self.draw_frame(self.focus_frame_colour)

            # Removing hint if focused:
            if self.hint_active:
                self.set_text_string("")
                self.hint_active = False

            key_down_events = GAME.get_key_down_events()

            if len(key_down_events) > 0:

                # Iterating through each key down event
                # because if multiple keys are pressed within a single frame,
                # all keys need to be registered:
                for key in key_down_events:

                    if key == pygame.K_BACKSPACE:
                        self.set_text_string(self.text_string[:-1])

                    elif key == pygame.K_RETURN:
                        self.focused = False
                    elif (len(self.text_string) < self.max_length) and self.input_type_allowed(key):

                        self.set_text_string(self.text_string + chr(key).upper())
        else:
            if len(self.text_string) == 0 and not self.focused:
                self.hint_active = True
                self.set_text_string(self.hint)

            # If the EditText is not in focus, it should be drawn just like a button:
            super().draw()

        # Calculating new frame based on new text size:

        self.rect = self.text.get_rect(center=(GAME.metre_to_pixel_point(self.location)))

        text_size = GAME.pixel_to_metre_point(self.text.get_size())

        self.size = [item + self.padding for item in text_size]

        # Tentative location value [0,0], corrected after:
        self.frame = pygame.Rect([0, 0], GAME.metre_to_pixel_point(self.size))
        self.frame.center = GAME.metre_to_pixel_point(self.location)

        self.draw_text(text_colour)

    def unfocused(self):
        # Now unfocused if mouse clicked anywhere else, or if it was focused and return has been clicked:
        return (not self.frame.collidepoint(pygame.mouse.get_pos()) and GAME.mouse_released()) \
               or (self.focused and pygame.K_RETURN in GAME.get_key_down_events())

    def input_type_allowed(self, key):

        # Wrapping in try-catch since some keys do not have a string value:
        try:
            key_string = chr(key)

            if self.input_type == self.STRING:
                return True
            elif self.input_type == self.INTEGER:
                return key_string.isnumeric()
            elif self.input_type == self.FLOAT:
                if key_string == ".":
                    return True
                else:
                    return key_string.isnumeric()

        except ValueError:
            return False

    def input_empty(self):
        return self.text_string == ""

    def get_hint(self):
        return self.hint

    def set_hint(self, hint):
        self.hint = hint


class Slider(View):

    def __init__(self, bar_size=(2, 0.075), handle_radius=0.1,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 margin=0.25, padding=0.5,
                 corner_radius=0.1, start_value=(0, 0),
                 slide_horizontal=True, slide_vertical=False,
                 bar_colour=SILVER, handle_colour=BLACK,
                 handle_hover_colour=IRIS):

        # Ensuring start values are locked to the middle if the slider can't slide that way.
        start_value = list(start_value)
        if not slide_horizontal: start_value[0] = 0.5
        if not slide_vertical: start_value[1] = 0.5

        super().__init__(bar_size, location=location, above=above, below=below, to_right_of=to_right_of,
                         to_left_of=to_left_of,
                         margin=margin, padding=padding)

        self.bar_size = bar_size
        self.handle_radius = handle_radius

        self.bar_colour = bar_colour
        self.handle_colour = handle_colour
        self.handle_hover_colour = handle_hover_colour

        self.corner_radius = corner_radius

        self.image = pygame.Surface(GAME.metre_to_pixel_point(self.size))
        self.image.fill(bar_colour)

        self.rect = self.image.get_rect()
        self.rect.center = GAME.metre_to_pixel_point(self.location)

        self.slide_horizontal = slide_horizontal
        self.slide_vertical = slide_vertical
        self.value = start_value

        self.bar = pygame.Rect([0, 0], GAME.metre_to_pixel_point(self.bar_size))
        self.bar.center = GAME.metre_to_pixel_point(self.location)

        self.handle_held = False

        self.handle = pygame.Rect([0, 0], GAME.metre_to_pixel_point([self.handle_radius * 2, self.handle_radius * 2]))
        self.handle.center = self.value_to_handle_position()

    def value_to_handle_position(self):
        return [int((self.value[0] * GAME.metre_to_pixel(self.bar_size[0])) + self.bar.bottomleft[0]),
                (int(self.bar.bottomleft[1] - GAME.metre_to_pixel(self.value[1]) * self.bar_size[1]))]

    def handle_position_to_value(self):
        return [(self.handle.centerx - self.bar.bottomleft[0]) / GAME.metre_to_pixel(self.bar_size[0]),
                (self.bar.bottomleft[1] - self.handle.centery) / GAME.metre_to_pixel(self.bar_size[1])]

    def draw_bar(self):
        pygame.draw.rect(GAME.get_screen(), self.bar_colour, self.bar,
                         border_radius=GAME.metre_to_pixel(self.corner_radius))

    def draw_handle(self, colour):

        if self.handle_grabbed():
            self.handle_held = True
        elif self.handle_released():
            self.handle_held = False

        if self.handle_held:
            # If the mouse is outside the Slider, still draw handle within the Slider:
            if self.slide_horizontal:
                self.handle.centerx = pygame.mouse.get_pos()[0]

                if self.handle.centerx < self.bar.midleft[0]:
                    self.handle.centerx = self.bar.midleft[0]
                elif self.handle.centerx > self.bar.midright[0]:
                    self.handle.centerx = self.bar.midright[0]
            else:
                self.handle.centerx = self.bar.centerx

            if self.slide_vertical:
                self.handle.centery = pygame.mouse.get_pos()[1]

                if self.handle.centery < self.bar.midtop[1]:
                    self.handle.centery = self.bar.midtop[1]
                elif self.handle.centery > self.bar.midbottom[1]:
                    self.handle.centery = self.bar.midbottom[1]
            else:
                self.handle.centery = self.bar.centery

            self.value = self.handle_position_to_value()

        self.value_to_handle_position()
        pygame.draw.circle(GAME.get_screen(), colour,
                           self.handle.center,
                           GAME.metre_to_pixel(self.handle_radius))

    def draw(self):
        # Determining correct handle colour
        if self.hovering():
            handle_colour = self.handle_hover_colour
        else:
            handle_colour = self.handle_colour

        self.draw_bar()
        self.draw_handle(handle_colour)

    def hovering(self):
        mouse_pos = pygame.mouse.get_pos()

        if ((self.handle.centerx - mouse_pos[0]) ** 2 + (
                self.handle.centery - mouse_pos[1]) ** 2) ** 0.5 <= GAME.metre_to_pixel(self.handle_radius):
            return True
        return False

    def handle_grabbed(self):
        return self.hovering() and GAME.mouse_pressed()

    def handle_released(self):
        return self.handle_held and GAME.mouse_released()

    def get_value(self):
        return self.value


class Player(pygame.sprite.Sprite):

    def __init__(self, player_id, name, inventory):
        super().__init__()

        self.id = player_id
        self.name = name
        self.inventory = inventory

    def get_id(self): return self.id

    def set_id(self, player_id): self.id = player_id

    def get_name(self): return self.name

    def set_name(self, name): self.name = name

    def get_inventory(self): return self.inventory

    def set_inventory(self, inventory): self.inventory = inventory


class DatabaseHelper:
    FRAME_RATE = 0
    SHOW_FRAME_RATE = 1
    VOLUME = 2

    def __init__(self):

        self.DB = "saves.db"

        # Checking that the database does not already exist:
        if os.path.isfile(self.DB): return

        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # Players table stores the players, the progress of whom are separate:
        cursor.execute("""CREATE TABLE IF NOT EXISTS PLAYERS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            NAME TEXT NOT NULL
                        )""")

        # Items table stores item types and their descriptions:
        cursor.execute("""CREATE TABLE IF NOT EXISTS ITEMS(
                                    NAME TEXT PRIMARY KEY NOT NULL,
                                    DESCRIPTION TEXT NOT NULL
                               )""")

        # Inserting item types that are in the game:
        cursor.executemany("INSERT INTO ITEMS VALUES(?, ?)", [(LIVES, DESC_LIVES), (COINS, DESC_COINS)])

        # Inventory Items table stores every item in the inventory of every player alongside their quantity:
        cursor.execute("""CREATE TABLE IF NOT EXISTS INVENTORY_ITEMS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            PLAYER_ID INTEGER NOT NULL,
                            NAME TEXT NOT NULL,
                            QUANTITY INTEGER NOT NULL
                        )""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS SETTINGS(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            TYPE INTEGER NOT NULL,
                            VALUE REAL NOT NULL        
                        )""")

        connection.commit()
        connection.close()

    def get_player(self, player_id):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM PLAYERS WHERE ID = ?", [player_id])
        result = cursor.fetchone()

        player = Player(result[0], result[1], self.get_player_inventory(player_id))

        connection.commit()
        connection.close()

        return player

    def save_player(self, player):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # First, checking if the player is already in the database, then adding or updating accordingly:
        cursor.execute("SELECT * FROM PLAYERS WHERE ID = ?", [player.get_id()])
        if len(cursor.fetchall()) > 0:
            # The player is already present, just needs to be updated:
            cursor.execute("UPDATE PLAYERS SET NAME = ? WHERE ID = ?", (player.get_name(), player.get_id()))

            player_id = player.get_id()

        else:
            # The player is not present, needs to be added:
            cursor.execute("INSERT INTO PLAYERS VALUES(NULL, ?)", [player.get_name()])

            # Retrieving the ID of the player such that it can be set to the player instance:
            cursor.execute("SELECT last_insert_rowid()")
            player_id = cursor.fetchone()[0]

            player.set_id(player_id)

        connection.commit()
        connection.close()

        # The inventory of the player also needs to be added:
        self.save_player_inventory(player)

        # Returning the ID of the player just added:
        return player_id

    def get_player_inventory(self, player_id):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM INVENTORY_ITEMS WHERE PLAYER_ID = ?", [player_id])

        inventory = {}

        for item in cursor.fetchall():
            inventory[item[2]] = item[3]

        connection.commit()
        connection.close()
        return inventory

    def save_player_inventory(self, player):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        inventory = player.get_inventory()

        for key in inventory:
            # First, checking if the item is in the table, then adding or updating accordingly:
            cursor.execute("SELECT * FROM INVENTORY_ITEMS WHERE NAME = ? AND PLAYER_ID = ?", [key, player.get_id()])
            if len(cursor.fetchall()) > 0:
                # The item is already present, just the quantity needs to be updated:
                cursor.execute("UPDATE INVENTORY_ITEMS SET QUANTITY = ? WHERE NAME = ? AND PLAYER_ID = ?",
                               [inventory[key], key, player.get_id()])
            else:
                # The item is not present, the item itself needs to be added:
                cursor.execute("INSERT INTO INVENTORY_ITEMS VALUES(NULL, ?, ?, ?)",
                               [player.get_id(), key, inventory[key]])

        connection.commit()
        connection.close()

    def get_item_description(self, item_name):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT DESCRIPTION FROM ITEMS WHERE NAME = ?", [item_name])

        result = cursor.fetchone()[0]

        print(result)

        connection.commit()
        connection.close()

        return result

    def get_frame_rate(self):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT VALUE FROM SETTINGS WHERE TYPE=?", [self.FRAME_RATE])

        cursor_return = cursor.fetchone()
        if cursor_return is not None:
            result = int(cursor_return[0])
        else:
            result = None

        connection.commit()
        connection.close()

        return result

    def set_frame_rate(self, frame_rate):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # First, checking if the necessary record is in the table, then adding or updating accordingly:
        cursor.execute("SELECT VALUE FROM SETTINGS WHERE TYPE=?", [self.FRAME_RATE])
        if len(cursor.fetchall()) > 0:
            # The record is already present, just the value needs to be updated:
            cursor.execute("UPDATE SETTINGS SET VALUE = ? WHERE TYPE = ? ", [frame_rate, self.FRAME_RATE])
        else:
            # The record is not present, the record itself needs to be added:
            cursor.execute("INSERT INTO SETTINGS VALUES(NULL, ?, ?)", [self.FRAME_RATE, frame_rate])

        connection.commit()
        connection.close()

    # TODO: SINCE SETTINGS ARE NOW THE SAME DATA TYPE, ONE FUNCTION FOR ALL OF THEM?? YES BUT LATER
    def get_show_frame_rate(self):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT VALUE FROM SETTINGS WHERE TYPE=?", [self.SHOW_FRAME_RATE])

        cursor_return = cursor.fetchone()
        if cursor_return is not None:
            result = int(cursor_return[0]) == 1
        else:
            result = None

        connection.commit()
        connection.close()

        return result

    def set_show_frame_rate(self, value):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # First, checking if the necessary record is in the table, then adding or updating accordingly:
        cursor.execute("SELECT VALUE FROM SETTINGS WHERE TYPE=?", [self.SHOW_FRAME_RATE])
        if len(cursor.fetchall()) > 0:
            # The record is already present, just the value needs to be updated:
            cursor.execute("UPDATE SETTINGS SET VALUE = ? WHERE TYPE = ? ", [value, self.SHOW_FRAME_RATE])
        else:
            # The record is not present, the record itself needs to be added:
            cursor.execute("INSERT INTO SETTINGS VALUES(NULL, ?, ?)", [self.SHOW_FRAME_RATE, value])

        connection.commit()
        connection.close()

    def get_volume(self):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        cursor.execute("SELECT VALUE FROM SETTINGS WHERE TYPE=?", [self.VOLUME])

        cursor_return = cursor.fetchone()
        if cursor_return is not None:
            result = float(cursor_return[0])
        else:
            result = None

        connection.commit()
        connection.close()

        return result

    def set_volume(self, value):
        connection = sqlite3.connect(self.DB)
        cursor = connection.cursor()

        # First, checking if the necessary record is in the table, then adding or updating accordingly:
        cursor.execute('SELECT VALUE FROM SETTINGS WHERE TYPE=?', [self.VOLUME])
        if len(cursor.fetchall()) > 0:
            # The record is already present, just the value needs to be updated:
            cursor.execute("UPDATE SETTINGS SET VALUE = ? WHERE TYPE = ? ", [value, self.VOLUME])
        else:
            # The record is not present, the record itself needs to be added:
            cursor.execute("INSERT INTO SETTINGS VALUES(NULL, ?, ?)", [self.VOLUME, value])

        connection.commit()
        connection.close()


HD = [1280, 720]
FHD = [1920, 1080]
QHD = [2160, 1440]
UHD = [3840, 2160]

GAME = Game()
GAME.start()
