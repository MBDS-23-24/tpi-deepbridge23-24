class Coeff_Strategy:

    def __int__(self):
        pass

    def eval_coeff_by_max_dist(self, d1, d2):
        if d1 > d2:
            return (1, 0)
        return (0, 1)

    def eval_coeff_by_min_dist(self, d1, d2):
        self.eval_coeff_by_max_dist(d2, d1)

    def pourcentage_pixel(self, d1, d2):

        d = d1 + d2
        c1 = d - (d1 / d)
        c2 = d - (d2 / d)

        return c1, c2


