from colours import *
from strings import *
from abc import ABC, abstractmethod
import pygame



# TODO: Pass constructor values in the abstract unit. They should immediately be converted to pixels and worked in that way.
#  Margin, padding and font size to be passed in abstract units and immediately converted to pixels as well!

# TODO: The unit rectangle is not centred!!!! - This is not that important, since location is to be passed in pixels.

# TODO: Location not passed in constructor if not relation. We can just set its rect.topleft etc. to another rect value ! YES!

# An abstract class which all the UI elements inherit from:
class View(ABC, pygame.sprite.Sprite):
    # When the frame (border / background) of the UI element should be shown:
    NEVER = 0
    ALWAYS = 1
    HOVER = 2
    FOCUS = 3

    @abstractmethod
    def __init__(self, game, size=(0, 0),
                 location=(0, 0), above=None, below=None, to_left_of=None, to_right_of=None, centre_between=None,
                 margin=0.02, padding=0.04,
                 frame_condition=NEVER, frame_thickness=0.005, corner_radius=0.01,
                 frame_colour=BLACK, frame_hover_colour=SMOKE):

        super().__init__()

        # The game is passed as an attribute to access its attributes and methods:
        self.game = game

        # The display surface:
        self.display = pygame.display.get_surface()

        # Padding and margin in arbitrary units:
        self.margin = margin
        self.padding = padding

        # When the frame should be shown:
        self.frame_condition = frame_condition
        # The colour of the frame:
        self.frame_colour = frame_colour
        self.frame_hover_colour = frame_hover_colour
        # The thickness and corner radius of the frame:
        self.thickness = frame_thickness
        self.corner_radius = corner_radius

        # If a size value has been passed, setting it:
        self.size = None
        self.set_size(size)

        self.rect = None

        # The UI elements that have a relationship with this one:
        # These fields can be used to position UI elements by describing its relationship to another,
        # rather than explicitly using a location:
        self.above = above
        self.below = below
        self.to_left_of = to_left_of
        self.to_right_of = to_right_of

        if above is not None:
            self.place_above(above)
        elif below is not None:
            self.put_below(below)
        elif to_left_of is not None:
            self.place_to_left_of(to_left_of)
        elif to_right_of is not None:
            self.place_to_right_of(to_right_of)
        elif centre_between is not None:
            self.centre_between(centre_between)
        else:
            self.location = location

        # Tentative location value (0,0), corrected afterwards:
        self.frame_rect = pygame.Rect((0, 0), self.game.unit_to_pixel_point(self.size))
        self.frame_rect.center = self.game.unit_to_pixel_point(self.location)

    def get_rect(self):
        return self.rect

    def get_location(self):
        return self.location

    def get_margin(self):
        return self.margin

    def get_padding(self):
        return self.padding

    def get_size(self):
        return self.size

    def set_size(self, size):
        # Setting accurate size including padding in arbitrary units:
        self.size = [dimension + self.padding for dimension in size]

    def place_above(self, view):
        # Placing the current UI element above the stated UI element, taking into account margins:
        view_location = view.get_location()
        self.location = [view_location[0],
                         view_location[1] - 0.5 * self.size[1] - 0.5 * view.get_size()[
                             1] - self.margin - view.get_margin()]

    def put_below(self, view):
        # Placing the current UI element below the stated UI element, taking into account margins:
        view_location = view.get_location()
        self.location = [view_location[0],
                         view_location[1] + 0.5 * self.size[1] + 0.5 * view.get_size()[
                             1] + self.margin + view.get_margin()]

    def place_to_left_of(self, view):
        # Placing the current UI element to the left of the stated UI element, taking into account margins:
        view_location = view.get_location()
        self.location = [
            view_location[0] - 0.5 * self.size[0] - 0.5 * view.get_size()[0] - self.margin - view.get_margin(),
            view_location[1]]

    def place_to_right_of(self, view):
        # Placing the current UI element to the right of the stated UI element, taking into account margins:
        view_location = view.get_location()
        self.location = [
            view_location[0] + 0.5 * self.size[0] + 0.5 * view.get_size()[
                0] + self.margin + view.get_margin(),
            view_location[1]]

    def centre_between(self, centre_between):
        # Places the UI element to the centre of 2 pre-existing UI elements
        location_1 = centre_between[0]
        location_2 = centre_between[1]

        self.location = (location_1[0] + location_2[0]) / 2, (location_1[1] + location_2[1]) / 2

    def draw_frame(self, colour):
        # Drawing the frame of the UI element:
        pygame.draw.rect(self.display, colour, self.frame_rect, self.game.unit_to_pixel(self.thickness),
                         self.game.unit_to_pixel(self.corner_radius))

    def draw(self):
        if self.hovering():
            if self.frame_condition != self.NEVER:
                self.draw_frame(self.frame_hover_colour)
        elif self.frame_condition == self.ALWAYS:
            self.draw_frame(self.frame_colour)

    def hovering(self):
        return self.frame_rect.collidepoint(pygame.mouse.get_pos())

    def clicked(self):
        return self.hovering() and self.game.mouse_released()


class TextLine(View):

    def __init__(self, game, text_string, font_size=0.08,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 centre_between=None,
                 margin=0.02, padding=0.04,
                 frame_condition=View.NEVER, frame_thickness=0.005, corner_radius=0.01,
                 frame_colour=BLACK, text_colour=BLACK, frame_hover_colour=BLACK, text_hover_colour=BLACK):

        # Attributes of the text itself:
        self.font_size = font_size
        self.font = game.get_font(self.font_size)
        self.text_string = str(text_string)
        self.text = self.font.render(self.text_string, True, text_colour)


        # The colour of the text:
        self.text_colour = text_colour
        self.text_hover_colour = text_hover_colour

        super().__init__(game, size=game.pixel_to_unit_point(self.text.get_size()),
                         location=location, above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of,
                         centre_between=centre_between,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         frame_colour=frame_colour, frame_hover_colour=frame_hover_colour)

        if self.location is not None:
            self.update_size()

    def centre_between(self, centre_between):
        super().centre_between(centre_between)
        self.update_size()

    def get_text(self):
        return self.text_string

    def set_text(self, text_string):
        self.text_string = text_string
        # Updating the text:
        self.text = self.font.render(str(self.text_string), True, self.text_colour)
        # Calculating new size:
        self.update_size()

    def update_size(self):
        # Calculating the size of the frame based on the text size:
        self.rect = self.text.get_rect(center=(self.game.unit_to_pixel_point(self.location)))
        self.set_size(self.game.pixel_to_unit_point(self.text.get_size()))
        # Tentative location value (0,0), corrected afterwards:
        self.frame_rect = pygame.Rect((0, 0), self.game.unit_to_pixel_point(self.size))
        self.frame_rect.center = self.game.unit_to_pixel_point(self.location)

    def draw_text(self, colour):
        self.display.blit(self.font.render(str(self.text_string), True, colour), self.rect)

    def draw(self):
        super().draw()
        if self.hovering():
            self.draw_text(self.text_hover_colour)
        else:
            self.draw_text(self.text_colour)


    def set_text_color(self, text_colour):
        self.text = self.font(self.font_size).render(self.text_string, True, text_colour)

    def set_italic(self, value):
        self.font.set_italic(value)
        self.text = self.font.render(self.text_string, True, self.text_colour)
        self.update_size()

    def set_bold(self, value):
        self.font.set_bold(value)
        self.text = self.font.render(self.text_string, True, self.text_colour)
        self.update_size()

    def set_underline(self, value):
        self.font.set_underline(value)
        self.text = self.font.render(self.text_string, True, self.text_colour)
        self.update_size()


class Text(View):

    def __init__(self, game, text_string, font_size=0.08,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None,
                 centre_between=None,
                 margin=0.02, padding=0.04,
                 frame_condition=View.NEVER, frame_thickness=0.005, corner_radius=0.01,
                 frame_colour=BLACK, text_colour=BLACK, frame_hover_colour=BLACK, text_hover_colour=BLACK):

        super().__init__(game, "",
                         location=location, above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of,
                         centre_between=centre_between,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         frame_colour=frame_colour, frame_hover_colour=frame_hover_colour)

        self.text_string_lines = text_string.split("\n")

        self.texts = []
        for index, item in enumerate(self.text_string_lines):

            if index == 0:
                text_line = TextLine(game, item,
                                     font_size=font_size,
                                     location=self.game.pixel_to_unit_point(self.rect.midtop),
                                     padding=0)
            else:
                text_line = TextLine(game, item, font_size=font_size, below=self.texts[index-1], padding=0)

            self.texts.append(text_line)

        self.update_size()

    def update_size(self):
        width = 0
        height = 0

        for text in self.texts:
            margin_and_padding_px = self.game.unit_to_pixel(text.get_margin()) + self.game.unit_to_pixel(text.get_padding())
            text_width = text.get_rect().w + margin_and_padding_px
            text_height = text.get_rect().h + margin_and_padding_px
            if text_width > width:
                width = text_width
            height += text_height

        self.rect.size = (width, height)

        self.frame_rect = pygame.Rect((0, 0), self.rect.size)
        self.frame_rect.center = self.rect.center



    def draw(self):
        super().draw()
        for text in self.texts:
            text.draw_text()





class Image(View):

    def __init__(self, game, icon, size=(0.1, 0.1),
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None, centre_between=None,
                 margin=0.02, padding=0.04,
                 frame_condition=View.NEVER, frame_thickness=0.005, corner_radius=0.01,
                 frame_colour=BLACK,
                 frame_hover_colour=BLACK):

        super().__init__(game, size=size,
                         location=location, above=above, below=below, to_right_of=to_right_of, to_left_of=to_left_of,
                         centre_between=centre_between,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         frame_colour=frame_colour, frame_hover_colour=frame_hover_colour)

        # Setting up the image icon:
        self.icon = None
        self.icon_rect = None
        # The maximum size of the icon - the size of the button without padding:
        self.max_icon_size = size
        self.set_icon(icon)

    def update_icon_size(self):
        # Updating the icon size whilst maintaining its aspect ratio:
        current_icon_size_px = self.icon.get_size()
        max_icon_size_px = self.game.unit_to_pixel_point(self.max_icon_size)
        icon_width = current_icon_size_px[0]
        icon_height = current_icon_size_px[1]

        if icon_width > icon_height:
            scale_factor = max_icon_size_px[0] / icon_width
            icon_width = max_icon_size_px[0]
            icon_height *= scale_factor
        else:
            scale_factor = max_icon_size_px[1] / icon_height
            icon_height = max_icon_size_px[1]
            icon_width *= scale_factor

        # Setting the icon with the adjusted size:
        self.icon = pygame.transform.scale(self.icon, (icon_width, icon_height))

    def set_icon(self, icon):
        self.icon = icon
        self.update_icon_size()
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.center = self.game.unit_to_pixel_point(self.location)

    def draw(self):
        super().draw()
        self.display.blit(self.icon, self.icon_rect)


# Simply creates an instance of the correct UI object and uses
# the correct default values for implementing the UI object as a button:
class Button(View):

    def __init__(self, game, text_string=None, font_size=0.08, icon=None, size=(0.1, 0.1), location=(0, 0), above=None,
                 below=None, to_right_of=None, to_left_of=None, centre_between=None, margin=0.02, padding=0.04,
                 frame_condition=View.HOVER, frame_thickness=0.005, corner_radius=0.01, frame_colour=BLACK,
                 text_colour=BLACK, frame_hover_colour=SMOKE, text_hover_colour=SMOKE):

        super().__init__(game, size, location, above, below, to_right_of, to_left_of, centre_between, margin, padding,
                         frame_condition, frame_thickness, corner_radius, frame_colour, frame_hover_colour)

        if text_string is not None:
            # The button is a text button:
            self.target = TextLine(game, text_string, font_size=font_size,
                                   location=location, above=above, below=below, to_right_of=to_right_of,
                                   to_left_of=to_left_of, centre_between=centre_between,
                                   margin=margin, padding=padding,
                                   frame_condition=frame_condition, frame_thickness=frame_thickness,
                                   corner_radius=corner_radius,
                                   frame_colour=frame_colour, text_colour=text_colour,
                                   frame_hover_colour=frame_hover_colour,
                                   text_hover_colour=text_hover_colour)
        elif icon is not None:
            # The button is an image button:
            self.target = Image(game, icon, size=size,
                                location=location, above=above, below=below, to_right_of=to_right_of,
                                to_left_of=to_left_of,
                                centre_between=centre_between,
                                margin=margin, padding=padding,
                                frame_condition=frame_condition, frame_thickness=frame_thickness,
                                corner_radius=corner_radius,
                                frame_colour=frame_colour, frame_hover_colour=frame_hover_colour)

        self.__dict__.update(self.target.__dict__)

    def draw(self):
        self.target.draw()


class Slider(View):

    def __init__(self, game, bar_size=(0.2, 0.005), handle_radius=0.01, start_value=(0, 0),
                 slide_horizontal=True, slide_vertical=False,
                 location=(0, 0), above=None, below=None, to_right_of=None, to_left_of=None, centre_between=None,
                 margin=0.02, padding=0,
                 bar_colour=SILVER, handle_colour=BLACK, handle_hover_colour=IRIS):

        # The slider can have values between 0-1 for each axis.
        # Ensuring that the slider is centered on a given axis if it cannot slide on that axis:
        start_value = list(start_value)
        if not slide_horizontal: start_value[0] = 0.5
        if not slide_vertical: start_value[1] = 0.5

        self.slide_horizontal = slide_horizontal
        self.slide_vertical = slide_vertical
        self.value = start_value

        super().__init__(game, size=bar_size,
                         location=location, above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of,
                         centre_between=centre_between,
                         margin=margin, padding=padding)

        self.bar_size = bar_size
        self.handle_radius = handle_radius

        self.bar_colour = bar_colour
        self.handle_colour = handle_colour
        self.handle_hover_colour = handle_hover_colour

        # The slider bar:
        self.image = pygame.Surface(game.unit_to_pixel_point(self.bar_size))
        self.image.fill(bar_colour)

        # The slider rectangle:
        self.rect = self.image.get_rect()
        self.rect.center = self.game.unit_to_pixel_point(self.location)

        # Tentative location value (0,0), corrected afterwards:
        self.bar = pygame.Rect((0, 0), game.unit_to_pixel_point(self.bar_size))
        self.bar.center = game.unit_to_pixel_point(self.location)

        # Whether the handle of the slider is being held:
        self.handle_held = False

        # The slider handle:
        self.handle_rect = pygame.Rect([0, 0],
                                       game.unit_to_pixel_point([self.handle_radius * 2, self.handle_radius * 2]))
        self.handle_rect.center = self.value_to_handle_position()

    def value_to_handle_position(self):
        # Converts the value of the handle into the pixel position of the handle on-screen:
        return [int((self.value[0] * self.game.unit_to_pixel(self.bar_size[0])) + self.bar.bottomleft[0]),
                (int(self.bar.bottomleft[1] - self.game.unit_to_pixel(self.value[1]) * self.bar_size[1]))]

    def handle_position_to_value(self):
        # Converts the pixel position of the handle on-screen to its value:
        return [(self.handle_rect.centerx - self.bar.bottomleft[0]) / self.game.unit_to_pixel(self.bar_size[0]),
                (self.bar.bottomleft[1] - self.handle_rect.centery) / self.game.unit_to_pixel(self.bar_size[1])]

    def draw_bar(self):
        pygame.draw.rect(self.display, self.bar_colour, self.bar,
                         border_radius=self.game.unit_to_pixel(self.corner_radius))

    def draw_handle(self, colour):

        if self.handle_grabbed():
            self.handle_held = True
        elif self.handle_released():
            self.handle_held = False

        if self.handle_held:
            # If the pointer is outside the slider, the handle of the slider should still be bound by the bar:
            if self.slide_horizontal:
                self.handle_rect.centerx = pygame.mouse.get_pos()[0]

                if self.handle_rect.centerx < self.bar.midleft[0]:
                    self.handle_rect.centerx = self.bar.midleft[0]
                elif self.handle_rect.centerx > self.bar.midright[0]:
                    self.handle_rect.centerx = self.bar.midright[0]
            else:
                self.handle_rect.centerx = self.bar.centerx

            if self.slide_vertical:
                self.handle_rect.centery = pygame.mouse.get_pos()[1]

                if self.handle_rect.centery < self.bar.midtop[1]:
                    self.handle_rect.centery = self.bar.midtop[1]
                elif self.handle_rect.centery > self.bar.midbottom[1]:
                    self.handle_rect.centery = self.bar.midbottom[1]
            else:
                self.handle_rect.centery = self.bar.centery

            # Updating the value of the handle:
            self.value = self.handle_position_to_value()

        # Drawing the handle:
        pygame.draw.circle(self.display, colour,
                           self.handle_rect.center,
                           self.game.unit_to_pixel(self.handle_radius))

    def draw(self):
        self.draw_bar()

        # Drawing with the correct colour:
        if self.hovering():
            self.draw_handle(self.handle_hover_colour)
        else:
            self.draw_handle(self.handle_colour)

    def hovering(self):
        mouse_pos = pygame.mouse.get_pos()

        # Using the handle's radius to see if the mouse cursor is colliding with the handle:
        if ((self.handle_rect.centerx - mouse_pos[0]) ** 2 + (
                self.handle_rect.centery - mouse_pos[1]) ** 2) ** 0.5 <= self.game.unit_to_pixel(self.handle_radius):
            return True
        return False

    def handle_grabbed(self):
        # Whether the handle has just been grabbed:
        return self.hovering() and self.game.mouse_pressed()

    def handle_released(self):
        # Whether the handle has just been grabbed:
        return self.handle_held and self.game.mouse_released()

    def get_value(self):
        return self.value


# A UI element that cycles through strings when clicked:
class Selector(TextLine):

    def __init__(self, game, selection_strings=(OFF, ON), start_index=0, font_size=0.08,
                 location=(0, 0), above=None, below=None, to_left_of=None, to_right_of=None, centre_between=None,
                 margin=0.02, padding=0.04,
                 frame_condition=View.HOVER, frame_thickness=0.005, corner_radius=0.01,
                 frame_colour=BLACK, text_colour=BLACK, frame_hover_colour=SMOKE, text_hover_colour=SMOKE):

        # Whether the slider has just been incremented:
        self.incremented = False

        # The strings the selector will cycle through:
        self.selection_strings = [str(string) for string in selection_strings]
        self.selection_index = start_index

        super().__init__(game, self.selection_strings[self.selection_index], font_size=font_size,
                         location=location, above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of,
                         centre_between=centre_between,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         frame_colour=frame_colour, text_colour=text_colour, frame_hover_colour=frame_hover_colour,
                         text_hover_colour=text_hover_colour)

    def draw(self):
        # Drawing is essentially identical to parent:
        self.set_text(self.get_state())
        super().draw()

    def increment(self):
        if self.selection_index < len(self.selection_strings) - 1:
            self.selection_index += 1
        else:
            self.selection_index = 0

        self.incremented = True

    def get_state(self):
        # It is necessary to update the state here.
        # if we didi not, when we call this function after the selector is clicked,
        # we would get the state just before the click.

        if self.clicked():

            if not self.incremented:
                # If the slider has just been clicked and not yet incremented, increment it:
                self.increment()

        else:
            self.incremented = False

        return self.selection_strings[self.selection_index]


class TextInput(TextLine):
    # Input Type:
    STRING = 0
    INTEGER = 1
    FLOAT = 2

    def __init__(self, game, text_string=None, font_size=0.08, max_length=50, hint=PLACEHOLDER, clear_on_focus=False,
                 input_type=STRING,
                 location=(0, 0), above=None, below=None, to_left_of=None, to_right_of=None, centre_between=None,
                 margin=0.02, padding=0.04,
                 frame_condition=View.ALWAYS, frame_thickness=0.005, corner_radius=0.01,
                 frame_colour=BLACK, text_colour=BLACK, frame_hover_colour=SMOKE, text_hover_colour=SMOKE,
                 frame_focus_colour=IRIS, text_focus_colour=IRIS):

        # The input type that is allowed:
        self.input_type = input_type

        # The text is displayed if the element is empty:
        self.hint = hint

        # The maximum length of text input:
        self.max_length = max_length

        # Whether to set input as hint and clear input field when unfocused.
        # Means that there is no need to delete previous input when entering new input.
        self.clear_on_focus = clear_on_focus

        # Whether the element is currently in focus:
        self.in_focus = False

        # The colours for when the element is in focus - it has been clicked and currently editing:
        self.focus_frame_colour = frame_focus_colour
        self.focus_text_colour = text_focus_colour

        # If there is no text already present, showing the hint:
        if text_string is None:
            text_string = hint
            # Whether the hint is currently being shown:
            self.hint_active = True
        else:
            self.hint_active = False

        super().__init__(game, text_string, font_size=font_size,
                         location=location, above=above, below=below, to_left_of=to_left_of, to_right_of=to_right_of,
                         centre_between=centre_between,
                         margin=margin, padding=padding,
                         frame_condition=frame_condition, frame_thickness=frame_thickness, corner_radius=corner_radius,
                         frame_colour=frame_colour, text_colour=text_colour, frame_hover_colour=frame_hover_colour,
                         text_hover_colour=text_hover_colour)

    def draw(self):

        # If option enabled and the element has just been unfocused,
        # setting text as hint and clearing the text field:

        if self.clear_on_focus and self.unfocused() and self.text_string != "":
            self.set_hint(self.text_string)
            self.set_text("")

        if self.clicked():
            self.in_focus = True
        elif self.unfocused():
            self.in_focus = False

        if self.in_focus:
            self.draw_frame(self.focus_frame_colour)
            self.draw_text(self.focus_text_colour)

            # Removing the hint so that text can be input:
            if self.hint_active:
                self.set_text("")
                self.hint_active = False

            keys = self.game.get_key_down_events()

            if len(keys) > 0:
                # Iterating through each key press because if multiple keys are
                # pressed in a single frame, all need to be registered:
                for key in keys:
                    if key == pygame.K_BACKSPACE:
                        # Deleting if backspace is pressed:
                        self.set_text(self.text_string[:-1])

                    elif (len(self.text_string) < self.max_length) and self.input_type_allowed(key):
                        # If the input field has not reached the maximum allowed length,
                        # and the key pressed is allowed, adding it to the text input:
                        self.set_text(self.text_string + chr(key).upper())

        else:
            if len(self.text_string) == 0 and not self.in_focus:
                # If the input length is 0 and the text is not in focus, showing hint:
                self.hint_active = True
                self.set_text(self.hint)

            # When not in focus, drawn just like parent:
            super().draw()



    def unfocused(self):
        # Whether the UI element has just lost focus:
        return ((not self.hovering()) and self.game.mouse_released()) \
               or pygame.K_RETURN in self.game.get_key_down_events()

    def input_type_allowed(self, key):
        # Wrapping in try-catch since some keys do not have a string value:
        try:
            key_string = chr(key)

            if self.input_type == self.STRING:
                # Any key corresponding to a string is allowed:
                return True
            elif self.input_type == self.INTEGER:
                # Any number is allowed.
                # We can know we have an integer because the floating point is not allowed:
                return key_string.isnumeric()
                # There won't be any need to input negative numbers, so not allowing that.
            elif self.input_type == self.FLOAT:
                # Any number or the floating point is allowed.
                return key_string == "." or key_string.isnumeric()

        except ValueError:
            # If key does not have a string value, not allowing:
            return False

    def input_empty(self):
        return self.text_string == ""

    def get_hint(self):
        return self.hint

    def set_hint(self, hint):
        self.hint = hint
