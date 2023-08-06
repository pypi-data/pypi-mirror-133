from .random_color_palette import RandomColorPalette
import os, random
from cairosvg import svg2png


class FunkyHorse():

    def __init__(self):
        self.__svg_list = []
        self.__create()

    def __create(self):
        self.__svg_list.clear()
        self.color_palette = RandomColorPalette()
        self.__svg_list.append("""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 2006.3 2006.3">\n""")
        self.__svg_list.append("""<defs><clipPath id="clip-path"><circle cx="1003.15" cy="1003.15" r="1003.15"/></clipPath>""")
        self.__svg_list.append(self.color_palette.generate_svg_style())
        self.__svg_list.append("</defs>")

        #Adds the background
        background = self.__choose_random_asset("assets\\background") 

        self.__add_to_list("assets\\background\\" + background)

        #Adds the BG Hair
        hair = self.__choose_random_asset("assets\\hair") 

        self.__add_to_list("assets\\hair\\{}\\bg.svg".format(hair))

        #Adds the left ear
        ears = self.__choose_random_asset("assets\\ears") 

        self.__add_to_list("assets\\ears\\{}\\bg.svg".format(ears))

        #Adds the main body
        body = self.__choose_random_asset("assets\\body") 

        self.__add_to_list("assets\\body\\" + body)

        #Adds the eyes
        eyes = self.__choose_random_asset("assets\\eyes") 

        self.__add_to_list("assets\\eyes\\" + eyes)

        #Adds the muzzle
        muzzle = self.__choose_random_asset("assets\\muzzle") 

        self.__add_to_list("assets\\muzzle\\" + muzzle)

        #Adds the FG Hair

        self.__add_to_list("assets\\hair\\{}\\fg.svg".format(hair))

        #Adds the right ear

        self.__add_to_list("assets\\ears\\{}\\fg.svg".format(ears))

        #adds the accessory
        if random.randrange(0,10) > 5 :
            accessory = self.__choose_random_asset("assets\\accessory") 

            self.__add_to_list("assets\\accessory\\" + accessory)

        self.__svg_list.append("</svg>")

    def __choose_random_asset(self,path):
        return random.choice(os.listdir( os.path.join(os.path.dirname(__file__),path)))

    def __add_to_list(self,path):
        try :
            with open(os.path.join(os.path.dirname(__file__),path)) as svg :
                self.__svg_list.append(svg.read())
        except :
            pass

    def __str__(self):

        """
        Returns the entire drawing by joining list elements.
        """

        return("".join(self.__svg_list))

    def save_svg(self, path):

        """
        Saves the SVG drawing to specified path.
        Let any exceptions propagate up to calling code.
        """

        f = open(path, "w+")

        f.write(self.__str__())

        f.close()
    
    def save_png(self, write_to):
        """
        Saves the PNG drawing to specified path.
        """
        svg2png( self.__str__(), write_to= write_to)




