''' AStoreParam --- action for multiple param storing '''
from w2p.classes.actions.action import Action


class AStoreParam(Action):
    ''' Store entire param in processor storage.
    You can store multiple parameters by this action. '''

    def do(self):
        super(AStoreParam, self)._add_to_result_(self.data)
