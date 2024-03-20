import Criteria


class CoeffStrategy:

    def __init__(self):
        pass

    @staticmethod
    def eval_coeff_by_density(criteria: Criteria):
        return criteria.div(criteria.sumall())
    
