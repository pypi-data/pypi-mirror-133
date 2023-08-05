import abc

class Renderer(abc.ABC):
    @abc.abstractmethod
    def render_all(self, canvas, entities):
        pass

    @abc.abstractmethod
    def clear_all(self, canvas, entities):
        pass

    @abc.abstractmethod
    def draw_entity(self, canvas, entities):
        pass

    @abc.abstractmethod
    def clear_entity(self, canvas, entity):
        pass
