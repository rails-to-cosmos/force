''' Assert equals '''

from w2p.classes.actions.action import Action


class AAssertEquals(Action):
    ''' Assert equals action class '''
    def do(self):
        try:
            tgt = int(self.target)
        except ValueError:
            tgt = 0

        try:
            dta = int(self.data)
        except ValueError:
            dta = 0

        result = tgt == dta

        if not result:
            super(AAssertEquals, self).register_error(
                Action.AE_ASSERTION_ERROR % (tgt, dta))
        else:
            super(AAssertEquals, self).register_info(
                Action.AE_ASSERTION_SUCCESS % (tgt, dta))
