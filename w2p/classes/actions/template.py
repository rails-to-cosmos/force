''' Templates for proper action creating '''

from w2p.classes.actions.action import Action


class ATemplate(Action):
    ''' Template action class '''

    def do(self):
        result = None
        super(ATemplate, self)._add_to_result_(result)
