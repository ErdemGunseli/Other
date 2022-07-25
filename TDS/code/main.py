import pygame
from pygame import mixer

from debug import *
from strings import *
from assets import *
from player import Player
from utils import *
from user_interface import *
from level import *
from database_helper import DatabaseHelper

# TODO: Cascading and moving views when one moves/changes size
# TODO: mixer.find_channel()

class Game:

    def __init__(self):
        pygame.init()
        mixer.init()

        # When True, game will end:
        self.done = False

        # A helper for the relational database:
        self.database_helper = DatabaseHelper()

        # Getting the current resolution of the physical screen:
        screen_info = pygame.display.Info()
        self.resolution = [screen_info.current_w, screen_info.current_h]
        self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        self.rect = self.screen.get_rect()
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()

        # Calculating window dimensions - this is an arbitrary unit to make everything fully resolution independent:
        if self.resolution[0] > self.resolution[1]:
            self.window_dimensions = [1 + self.resolution[1] / self.resolution[0], 1]
        else:
            self.window_dimensions = [1, 1 + self.resolution[1] / self.resolution[0]]

            # Getting the frame rate cap setting from the database:
        self.frame_rate = int(self.database_helper.get_setting(DatabaseHelper.FRAME_RATE_LIMIT))

        # Getting whether the frame rate should be displayed at the corner of the screen:
        self.show_frame_rate = self.database_helper.get_setting(DatabaseHelper.SHOW_FRAME_RATE)

        # Getting the audio volume level:
        self.audio_volume = self.database_helper.get_setting(DatabaseHelper.AUDIO_VOLUME)

        # Setting up level:
        level_id = self.database_helper.get_player_stats()[Player.CURRENT_LEVEL_ID]
        self.current_level = Level(self, level_id)

        # Setting up display:
        pygame.display.set_caption(GAME_NAME)
        self.clock = pygame.time.Clock()

        # The font of the game:
        self.font = FONT

        self.all_events = []
        self.key_down_events = []
        self.start_game()

    def start_game(self):
        self.main_menu()

    def update(self):
        self.get_input()

        if self.show_frame_rate:
            fps_text = TextLine(self,
                                str(int(self.clock.get_fps())),
                                location=[0.04, 0.04],
                                font_size=0.04)
            fps_text.draw()

    def quit(self):
        self.done = True

    def get_current_level(self):
        return self.current_level

    def get_database_helper(self):
        return self.database_helper

    def get_current_frame_rate(self):
        return self.clock.get_fps()

    def get_current_frame_time(self):
        return 1 / self.clock.get_fps()

    def get_frame_rate_cap(self):
        return self.frame_rate

    def set_frame_rate_cap(self, frame_rate):
        self.frame_rate = frame_rate
        self.database_helper.update_setting(DatabaseHelper.FRAME_RATE_LIMIT, frame_rate)

    def get_show_frame_rate(self):
        return self.show_frame_rate

    def set_show_frame_rate(self, show_frame_rate):
        self.show_frame_rate = show_frame_rate
        self.database_helper.update_setting(DatabaseHelper.SHOW_FRAME_RATE, show_frame_rate)

    def get_audio_volume(self):
        return self.audio_volume

    def set_audio_volume(self, audio_volume):
        self.audio_volume = audio_volume
        self.database_helper.update_setting(DatabaseHelper.AUDIO_VOLUME, audio_volume)
        mixer.music.set_volume(audio_volume)

    def get_key_down_events(self):
        return self.key_down_events

    def get_input(self):
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

    def get_rect(self):
        return self.rect

    def unit_to_pixel(self, value):
        # Conversion between pixels and arbitrary units:
        return int(value * (self.resolution[0] / self.window_dimensions[0]))

    def unit_to_pixel_point(self, values):
        return int(values[0] * (self.resolution[0] / self.window_dimensions[0])), \
               int(values[1] * (self.resolution[0] / self.window_dimensions[0]))

    def pixel_to_unit(self, value):
        return value / (self.resolution[0] / self.window_dimensions[0])

    def pixel_to_unit_point(self, values):
        return values[0] / (self.resolution[0] / self.window_dimensions[0]), \
               values[1] / (self.resolution[0] / self.window_dimensions[0])

    def get_font(self, size):
        # The size of the font in arbitrary units:
        return pygame.font.SysFont(self.font, int(size * (self.resolution[0] / self.window_dimensions[0])))

    def main_menu(self):

        views = []

        # Play Button:
        btn_play = Button(self,
                          text_string=PLAY_GAME,
                          location=self.pixel_to_unit_point(self.rect.center))
        views.append(btn_play)

        # Settings Button:
        btn_settings = Button(self,
                              text_string=SETTINGS,
                              below=btn_play)
        views.append(btn_settings)

        # Quit Button:
        btn_quit = Button(self,
                          text_string=QUIT,
                          below=btn_settings)
        views.append(btn_quit)

        # Title Text
        txt_title = TextLine(self,
                             text_string=GAME_NAME,
                             centre_between=(self.pixel_to_unit_point(self.rect.midtop),
                                             self.pixel_to_unit_point(btn_play.get_rect().midtop)),
                             frame_condition=View.ALWAYS,
                             font_size=0.25)
        txt_title.set_italic(True)
        views.append(txt_title)

        while not self.done:
            self.screen.fill(WHITE)

            if self.key_pressed(pygame.K_1):
                self.testing()

            # On Click:
            if btn_play.clicked():
                if self.database_helper.get_player_stats()[Player.MAX_HEALTH] == 0:
                    self.character_menu()

                self.show_game()
                return
            elif btn_settings.clicked():
                self.settings_menu()
                pass
            elif btn_quit.clicked():
                self.quit()

            for view in views: view.draw()
            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def settings_menu(self):
        views = []

        # Show Frame Rate Selector
        if self.show_frame_rate:
            start_index = 1
        else:
            start_index = 0

        sel_show_frame_rate = Selector(self,
                                       font_size=0.04,
                                       start_index=start_index,
                                       location=self.pixel_to_unit_point(self.rect.center))
        views.append(sel_show_frame_rate)

        # Show Frame Rate Text:
        txt_show_frame_rate = TextLine(self,
                                       SHOW_FRAME_RATE,
                                       font_size=0.04,
                                       to_left_of=sel_show_frame_rate)
        views.append(txt_show_frame_rate)

        # Max Frame Rate Input:
        edt_txt_frame_rate = TextInput(self,
                                       font_size=0.04,
                                       hint=str(self.frame_rate),
                                       clear_on_focus=True,
                                       input_type=TextInput.INTEGER,
                                       max_length=3,
                                       above=sel_show_frame_rate)
        views.append(edt_txt_frame_rate)

        # Frame Rate Text:
        txt_frame_rate = TextLine(self,
                                  FRAME_RATE_LIMIT,
                                  font_size=0.04,
                                  to_left_of=edt_txt_frame_rate)
        views.append(txt_frame_rate)

        # Resolution Value Text:
        txt_resolution_value = TextLine(self,
                                        RESOLUTION_FORMAT.format(*self.resolution),
                                        font_size=0.04,
                                        above=edt_txt_frame_rate,
                                        frame_condition=View.ALWAYS)
        views.append(txt_resolution_value)

        # Resolution Text:
        txt_resolution = TextLine(self,
                                  RESOLUTION,
                                  font_size=0.04,
                                  to_left_of=txt_resolution_value)
        views.append(txt_resolution)

        # Audio Volume Slider
        sl_audio_volume = Slider(self,
                                 below=sel_show_frame_rate,
                                 start_value=[self.audio_volume, 0])
        views.append(sl_audio_volume)

        # Audio Volume Text
        txt_audio_volume = TextLine(self,
                                    AUDIO_VOLUME,
                                    font_size=0.04,
                                    to_left_of=sl_audio_volume)
        views.append(txt_audio_volume)

        # Settings Text:
        txt_settings = TextLine(self,
                                SETTINGS,
                                centre_between=(self.pixel_to_unit_point(self.rect.midtop),
                                                self.pixel_to_unit_point(txt_resolution_value.get_rect().midtop)))

        views.append(txt_settings)

        # Save & Exit Button
        btn_exit = Button(self,
                          text_string=BACK,
                          font_size=0.04,
                          centre_between=(self.pixel_to_unit_point(sel_show_frame_rate.get_rect().midbottom),
                                          self.pixel_to_unit_point(self.rect.midbottom)))

        views.append(btn_exit)

        mixer.music.load(MAIN_MENU_MUSIC)
        mixer.music.set_volume(self.audio_volume)
        mixer.music.play(-1)

        while not self.done:
            self.screen.fill(WHITE)
            if self.key_pressed(pygame.K_ESCAPE):
                return

            # If the refresh rate has been changed and the input is not empty, set it to the attribute:
            if edt_txt_frame_rate.unfocused() and not edt_txt_frame_rate.input_empty():
                frame_rate = int(edt_txt_frame_rate.get_text())
                self.set_frame_rate_cap(frame_rate)

            # Changing the frame rate display if the frame rate selector is clicked:
            if sel_show_frame_rate.clicked():
                self.set_show_frame_rate(sel_show_frame_rate.get_state() == ON)

            # If the audio volume slider has been changed:
            if sl_audio_volume.handle_released():
                self.set_audio_volume(sl_audio_volume.get_value()[0])

            # Exit if exit button or escape clicked:
            if btn_exit.clicked() or self.key_pressed(pygame.K_ESCAPE):
                mixer.music.fadeout(500)
                return

            for view in views: view.draw()
            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def testing(self):
        print(self.database_helper.get_setting(DatabaseHelper.FRAME_RATE_LIMIT))
        print(self.database_helper.get_setting(DatabaseHelper.SHOW_FRAME_RATE))
        print(self.database_helper.get_setting(DatabaseHelper.AUDIO_VOLUME))

        views = []
        txt_1 = TextLine(self, "Testing",
                         location=self.pixel_to_unit_point(self.rect.center),
                         frame_condition=View.NEVER)
        views.append(txt_1)

        txt_2 = TextLine(self, "Hi There",
                         below=txt_1,
                         frame_condition=View.ALWAYS)
        views.append(txt_2)

        img = pygame.image.load("C:/Users/eguns/GitHub/Main/Pygame/TDS/assets/images/item_icons/armour_torso.png")
        btn_1 = Button(self, icon=img,
                       below=txt_2)
        views.append(btn_1)

        btn_2 = Button(self, text_string="HTHTH",
                       to_right_of=btn_1,
                       margin=0.1)
        views.append(btn_2)

        sl_1 = Slider(self,
                      bar_size=[0.1, 0.1],
                      start_value=[0.5, 0.5],
                      above=txt_1,
                      slide_horizontal=True,
                      slide_vertical=True,
                      padding=0)
        views.append(sl_1)

        txt_s1_val = TextLine(self,
                              "",
                              to_left_of=sl_1,
                              frame_condition=View.ALWAYS,
                              font_size=0.05,
                              margin=0.1)
        views.append(txt_s1_val)

        sl_2 = Slider(self, above=sl_1)
        views.append(sl_2)

        txt_s2_val = TextLine(self,
                              "",
                              to_left_of=sl_2,
                              frame_condition=View.ALWAYS,
                              font_size=0.05,
                              margin=0.1)
        views.append(txt_s2_val)

        sel_test = Selector(self, to_right_of=txt_1)
        views.append(sel_test)

        while not self.done:
            self.screen.fill(WHITE)
            if self.key_pressed(pygame.K_ESCAPE): return

            txt_s1_val.set_text([round(item, 2) for item in sl_1.get_value()])
            txt_s2_val.set_text(round(sl_2.get_value()[0], 2))

            for view in views: view.draw()
            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def character_menu(self):

        views = []

        sl_stats = Slider(self,
                          bar_size=[0.3, 0.3],
                          start_value=[0.5, 0.5],
                          centre_between=(self.pixel_to_unit_point(self.rect.center),
                                          self.pixel_to_unit_point(self.rect.midleft)),
                          slide_horizontal=True,
                          slide_vertical=True,
                          padding=0,
                          margin=0)
        views.append(sl_stats)

        img_health = Image(self,
                           icon=pygame.image.load(HEALTH_ICON).convert_alpha(),
                           above=sl_stats,
                           frame_condition=1)
        views.append(img_health)

        img_speed = Image(self,
                          icon=pygame.image.load(SPEED_ICON).convert_alpha(),
                          below=sl_stats,
                          frame_condition=1)
        views.append(img_speed)

        img_melee_damage = Image(self,
                                 icon=pygame.image.load(MELEE_DAMAGE_ICON).convert_alpha(),
                                 to_left_of=sl_stats,
                                 frame_condition=1)
        views.append(img_melee_damage)

        img_ranged_damage = Image(self,
                                  icon=pygame.image.load(RANGED_DAMAGE_ICON).convert_alpha(),
                                  to_right_of=sl_stats,
                                  frame_condition=1)
        views.append(img_ranged_damage)

        txt_test = TextLine(self,
                            "",
                            centre_between=(self.pixel_to_unit_point(self.rect.center),
                                            self.pixel_to_unit_point(self.rect.midright)))

        views.append(txt_test)

        txt_test = TextLine(self,
                            "",
                            centre_between=(self.pixel_to_unit_point(self.rect.center),
                                            self.pixel_to_unit_point(self.rect.midright)))
        views.append(txt_test)

        btn_continue = Button(self,
                              text_string=CONTINUE,
                              below=txt_test)

        views.append(btn_continue)

        min_health = 75
        max_health = 125

        min_speed = 3
        max_speed = 5

        min_ranged = 75
        max_ranged = 125

        min_melee = 75
        max_melee = 125

        while not self.done:
            self.screen.fill(WHITE)

            if self.key_pressed(pygame.K_ESCAPE):
                return

            txt_test.set_text([round(item, 2) for item in sl_stats.get_value()])

            if btn_continue.clicked():
                # TODO: SAVE PLAYER
                return

            for view in views: view.draw()
            self.update()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

    def show_game(self):
        background_colour = self.current_level.get_current_background_colour()
        views = []


        while not self.done:
            self.screen.fill(background_colour)

            if self.key_pressed(pygame.K_ESCAPE):
                self.main_menu()
                # TODO: SHOW PAUSE MENU


            self.current_level.update()
            self.update()
            for view in views: view.draw()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)


Game()
