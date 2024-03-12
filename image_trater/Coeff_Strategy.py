class Coeff_Strategy:

    def __init__(self):
        pass

    def eval_coeff_by_max_dist(self, distances):
        # Pour trouver la distance maximale
        max_dist = max(distances)
        # Créer une liste de coefficients où le coefficient est 1 pour la distance maximale et 0 pour les autres
        coeffs = [1 if dist == max_dist else 0 for dist in distances]
        return coeffs

    def eval_coeff_by_min_dist(self, distances):
        # Pour trouver la distance minimale
        min_dist = min(distances)
        coeffs = [1 if dist == min_dist else 0 for dist in distances]
        return coeffs
        
    def eval_coeff_by_avg_dist(self, distances):
        # Calcul la distance moyenne
        avg_dist = sum(distances) / len(distances)
        # Calcul les coeffs en fonction de l'écart par rapport à la moyenne
        total_dist = sum(distances)
        coeffs = [(total_dist - (dist / total_dist)) for dist in distances]
        return coeffs

    def eval_coeff_by_half_dist(self, distances):
        # Ici on donne aux dist les memes coeffs
        coeffs = [0.5 for _ in distances]
        return coeffs
    
