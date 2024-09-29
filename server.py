"""This file was copied over from the original Schelling mesa example."""

import mesa
from model import Schelling


def get_happy_agents(model):
    """
    Display a text count of how many happy agents there are.
    """
    return f"Happy agents: {model.happy}"


def schelling_draw(agent):
    """
    Portrayal Method for canvas
    """
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:  # Перший тип агента
        portrayal["Color"] = ["#FF0000", "#FF9999"]  # Червоний
        portrayal["stroke_color"] = "#00FF00"  # Зелена обводка
    elif agent.type == 1:  # Другий тип агента
        portrayal["Color"] = ["#00FF00", "#99FF99"]  # Зелений
        portrayal["stroke_color"] = "#FF0000"  # Червона обводка
    else:  # Інші типи агентів 
        portrayal["Color"] = ["#0000FF", "#9999FF"]  # Синій
        portrayal["stroke_color"] = "#000000"  # Чорна обводка
    return portrayal


canvas_element = mesa.visualization.CanvasGrid(
    portrayal_method=schelling_draw,  # Метод відображення агентів
    grid_width=30,                     # Ширина сітки 30 клітин
    grid_height=30,                    # Висота сітки 30 клітин
    canvas_width=800,                  # Ширина канвасу 800 пікселів
    canvas_height=800,                 # Висота канвасу 800 пікселів
)

happy_chart = mesa.visualization.ChartModule([
    {
        "Label": "happy",
        "Color": "Black",
        "stroke_width": 2,  # Змінено товщину лінії
        "LineStyle": "dashed"  # Змінено стиль лінії на пунктирний
    },
    {
        "Label": "unhappy",  # Додано графік для незадоволених агентів
        "Color": "Red",
        "stroke_width": 2,
    },
    {
        "Label": "Type 0 Agents",  # Додано графік для агентів типу 0
        "Color": "#FF0000",
        "stroke_width": 2,
    },
    {
        "Label": "Type 1 Agents",  # Додано графік для агентів типу 1
        "Color": "#0000FF",
        "stroke_width": 2,
    }
])


model_params = {
    "height": 30,  # Зміна висоти сітки з 20 на 30 для збільшення простору для агентів.
    "width": 30,   # Зміна ширини сітки з 20 на 30 для збільшення простору для агентів,
    "density": mesa.visualization.Slider(
        name="Agent density", value=0.6,  # Зменшено значення щільності агентів для тестування впливу на модель
        min_value=0.1, max_value=1.0, step=0.1
    ),
    "minority_pc": mesa.visualization.Slider(
        name="Fraction minority", value=0.25,  # Збільшено частку меншин для перевірки нових сценаріїв
        min_value=0.00, max_value=1.0, step=0.05
    ),
    "homophily": mesa.visualization.Slider(
        name="Homophily", value=3, min_value=0, max_value=8, step=1
    ),
    "radius": mesa.visualization.Slider(
        name="Search Radius", value=1, min_value=1, max_value=5, step=1
    ),
    "interaction_threshold": mesa.visualization.Slider(
        name="Interaction Threshold", value=0.5,  # Новий параметр для визначення порогу взаємодії агентів
        min_value=0.0, max_value=1.0, step=0.1
    ),
    "max_moves": mesa.visualization.Slider(
        name="Maximum Moves", value=5,  # Новий параметр для обмеження максимальної кількості рухів агента за один крок
        min_value=1, max_value=10, step=1
    ),
    "agent_color_type": mesa.visualization.Checkbox(
        name="Use Type Color", value=True,  # Новий параметр для вибору кольору агентів за типом
    ),
}

server = mesa.visualization.ModularServer(
    model_cls=Schelling,
    visualization_elements=[canvas_element, get_happy_agents, happy_chart],
    name="Schelling Segregation Model",
    model_params=model_params,
)
