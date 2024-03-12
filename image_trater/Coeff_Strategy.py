class Coeff_Strategy:

    def __int__(self):
        pass

    def eval_coeff_by_max_dist(self, d1, d2):
        if d1 > d2:
            return (1, 0)
        return (0, 1)

    def eval_coeff_by_min_dist(self, d1, d2):
        self.eval_coeff_by_max_dist(d2, d1)