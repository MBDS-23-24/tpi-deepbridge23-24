import Criteria


class Coeff_Strategy:

    def __init__(self):
        pass

    def eval_coeff_by_max(self, criteria: Criteria):
        # TODO: Rework
        [1] * len(criteria.get())

    def eval_coeff_by_min(self, criteria: Criteria):
        # TODO: Rework
        [1] * len(criteria.get())
        
    def eval_coeff_by_density(self, criteria: Criteria):
        ref_criteria = criteria.sumall()
        # Calcul de la moyenne
        coeffs = criteria.div(ref_criteria)
        return coeffs

    def eval_coeff_by_half(self, criteria: Criteria):
        coeffs = [0.5 for _ in criteria.get()]
        return coeffs
    
