import mesa

class SchellingAgent(mesa.Agent):
    """
    Schelling segregation agent.
    """

    def __init__(self, unique_id, model, agent_type):
        """
        Create a new Schelling agent.

        Args:
            unique_id: Unique identifier for the agent.
            model: The model the agent belongs to.
            agent_type: Indicator for the agent's type (minority=1, majority=0).
        """
        super().__init__(unique_id, model) 
        self.type = agent_type

    def step(self):
        similar = 0
        for neighbor in self.model.grid.iter_neighbors(
            self.pos, moore=True, radius=self.model.radius
        ):
            if neighbor.type == self.type:
                similar += 1

        # If unhappy, move:
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1


class Schelling(mesa.Model):
    """
    Model class for the Schelling segregation model.
    """

    def __init__(self, height=20, width=20, homophily=3, radius=1, 
                interaction_threshold=0.5, max_moves=5, agent_color_type=True,
                 density=0.8, minority_pc=0.3, seed=None):
        """
        Create a new Schelling model.

        Args:
            width, height: Size of the space.
            density: Initial chance for a cell to be populated.
            minority_pc: Chances for an agent to be in minority class.
            homophily: Minimum number of agents of the same class needed to be happy.
            radius: Search radius for checking similarity.
            seed: Seed for reproducibility.
        """
        super().__init__(seed=seed)
        self.height = height
        self.width = width
        self.density = density
        self.minority_pc = minority_pc
        self.homophily = homophily
        self.radius = radius
        self.interaction_threshold = interaction_threshold  # Додано новий параметр
        self.max_moves = max_moves  # Додано новий параметр
        self.agent_color_type = agent_color_type  # Додано новий параметр

        self.grid = mesa.space.SingleGrid(width, height, torus=True)

        self.happy = 0
        self.datacollector = mesa.DataCollector(
            model_reporters={"happy": "happy"},  
        )

        unique_id = 0 
        for _, pos in self.grid.coord_iter():
            if self.random.random() < self.density:
                agent_type = 1 if self.random.random() < self.minority_pc else 0
                agent = SchellingAgent(unique_id, self, agent_type)  
                self.grid.place_agent(agent, pos)
                unique_id += 1  

        self.datacollector.collect(self)

    def step(self):
        """
        Run one step of the model.
        """
        self.happy = 0  
        self.agents.shuffle_do("step")

        self.datacollector.collect(self)

        if self.happy == len(self.agents):
            self.running = False
