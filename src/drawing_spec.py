import dataclasses
from typing import Tuple
_PRESENCE_THRESHOLD = 0.5
_VISIBILITY_THRESHOLD = 0.5
_BGR_CHANNELS = 3

WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)


@dataclasses.dataclass
class DrawingRed:
    color: Tuple[int, int, int] = RED_COLOR
    # Thickness for drawing the annotation. Default to 2 pixels.
    thickness: int = 2
    # Circle radius. Default to 2 pixels.
    circle_radius: int = 2

class DrawingGreen:
    color: Tuple[int, int, int] = GREEN_COLOR
    # Thickness for drawing the annotation. Default to 2 pixels.
    thickness: int = 2
    # Circle radius. Default to 2 pixels.
    circle_radius: int = 2

class DrawingNeutral:
    color: Tuple[int, int, int] = BLACK_COLOR
    # Thickness for drawing the annotation. Default to 2 pixels.
    thickness: int = 2
    # Circle radius. Default to 2 pixels.
    circle_radius: int = 2

##Ova datoteka je samo uredena na djelovima kojima se dodavala boja, dok su ostali dijelovi koda ostavljeni neuredni jer nisu relevantni za funkcionalnost programa. Ovdje se definiraju različite boje i debljine linija koje se koriste za crtanje različitih dijelova tijela (ruke, lice, tijelo) u MediaPipe modelu. Također se definiraju stilovi crtanja za različite skupove točaka na rukama, licu i tijelu, što omogućava vizualno razlikovanje različitih dijelova tijela prilikom prikaza rezultata detekcije.