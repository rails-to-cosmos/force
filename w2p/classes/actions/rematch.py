''' re.match wrapper '''

import re

from w2p.classes.actions.action import Action


class AReMatch(Action):
    ''' Use re.match on target and store result in action data '''

    def do(self):
        pattern = self.data.get(Action.AD_PATTERN)
        names = self.data.get(Action.AD_NAMES)
        target = super(AReMatch, self).ensure_list(self.target)

        result = dict()
        for item in target:
            match_res = re.findall(pattern, item)

            if len(match_res) > 0:
                for group_id, group_val in enumerate(match_res):
                    if names:
                        self.data[names[group_id]] = group_val
                        result[names[group_id]] = group_val
                    else:
                        super(AReMatch, self)._add_to_result_(group_val)

        if len(result.keys()) > 0:
            super(AReMatch, self)._add_to_result_(result)
