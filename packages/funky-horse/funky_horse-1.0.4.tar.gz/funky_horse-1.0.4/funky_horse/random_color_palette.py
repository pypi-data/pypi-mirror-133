#This class generates the color palette used for the picture
import random


class RandomColorPalette():

    def __init__(self):
        self.colors = []
        self.colors_tuple = ()
        self.generate_palette()

    def get_random_color(self,pastel_factor = 0.6):
        return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]
    
    def color_distance(self,c1,c2):
        return sum([abs(x[0]-x[1]) for x in zip(c1,c2)])

    def generate_new_color(self,pastel_factor = 0.5):
        max_distance = None
        best_color = None
        for i in range(0,100):
            color = self.get_random_color(pastel_factor = pastel_factor)
            if not self.colors:
                self.colors.append(color)
                return
            best_distance = min([self.color_distance(color,c) for c in self.colors])
            if not max_distance or best_distance > max_distance:
                max_distance = best_distance
                best_color = color
        self.colors.append(best_color)

    def generate_palette(self,number = 10):
        for i in range(0,number):
            self.generate_new_color(pastel_factor = 0.7)
        for i in range(0,number):
            self.colors_tuple += (str((int(self.colors[i][0]*255), int(self.colors[i][1]*255), int(self.colors[i][2]*255))),)

    #Getter
    def get_color(self,number):
        return( (int(self.colors[number][0]*255), int(self.colors[number][1]*255), int(self.colors[number][2]*255)))

    def generate_svg_style(self):
        self.generate_palette
        style = """
        <style>
            .background-1{{fill:rgb{};clip-path:url(#clip-path)}}
            .background-2{{fill:rgb{};clip-path:url(#clip-path)}}
            .body-1{{fill:rgb{};clip-path:url(#clip-path)}}
            .body-2{{fill:rgb{};clip-path:url(#clip-path)}}
            .eye-1{{fill:rgb{};clip-path:url(#clip-path)}}
            .eye-2{{fill:rgb{};clip-path:url(#clip-path)}}
            .accessory-1{{fill:rgb{};clip-path:url(#clip-path)}}
            .accessory-2{{fill:rgb{};clip-path:url(#clip-path)}}
            .hair-1{{fill:rgb{};clip-path:url(#clip-path)}}
            .hair-2{{fill:rgb{};clip-path:url(#clip-path)}}
            </style>\n"""
        style = style.format(*self.colors_tuple)
        return(style)