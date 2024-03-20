import Criteria


class CoeffStrategy:

    def __init__(self):
        pass

    def eval_coeff_by_density(self, criteria: Criteria):
        return criteria.div(criteria.sumall())
    
