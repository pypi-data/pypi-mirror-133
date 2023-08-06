"""
Projet d'analyse: Sujet 31
Le projet: Il nous est demandé d'approcher la valeur de sin(8/5) tout en certifiant nos resultats.
            Cependant, avec la formule de Taylor
            sur R combinée a la preuve de Cauchy et a l'etablissement du certificat de convergence,
            on s'est vite rendu compte que l'on peut etendre cette definition sur R et ainsi pouvoir
            cette de maniere moduler a un ordre k les N premieres decimales du sin de tout reel.
            Ci-dessous, le programme informatique traduisant les resultats de nos analyses.
"""
"""
dans ce code python ,on realise le programme en une classe générale tout en definissant toutes les fonctions supplemntaires et celles demandées dans l'ennoncé 
et dans la deuxieme partie on aura le main pour pouvoir tester le programme 
"""

class classe_General:

    def __init__(self, val):
        """
        Initialisation de la fonction calsse_General pour les calculs ménant a sin(:param val)
        :param val: Valeur numerique de type float sur laquelle portera notre analyse
        """
        self.val = val
        pass
    
    def absolu(self, x):
        '''
        Fonction retournant la valeur absolue de :param x
        :param x: Valeur négative ou positive
        :return: La valeur absolue de :param x'''
        if x < 0:
            return x*-1
        else :
            return x

    def fonction_factorielle(self, x):
        """
        Fonction de calcul du fonction_factorielle de :param x
        :param x: Entier naturel dont on veut determiner le factoriel
        :return: Le factoriel de :param x
        """
        return 1 if x <= 1 else x * self.fonction_factorielle(x - 1)

    def fonction_tronque(self, x, pre):
        """
        Fonction tronquant :param x a 10 ** -:param precision  pres
        :param x: Flottant que l'on veut tronquer
        :param pre: pre de troncature souhaitee
        :return: :param x tronquee a 10 ** -:param precision pres
        """
        pre = 10 ** pre
        return (int(x * pre)) / pre

    def fonction_sinusTaylorien(self, angle, pre):
        """
        Fonction calculant la valeur de la definition de sin(:param angle) selont la formule de Taylor a
        l'ordre :param pre
        :param angle: flottant dont on souhaite obtenir le sin
        :param pre: l'ordre n du calcul du developpement limité menant a sin(:param angle)
        :return: sin(:param angle) selon le developpement limité de Taylor a l'ordre n=:param pre
        """
        v = 0.0
        for n in range(pre):
            v += (((-1) ** n) * ((angle ** ((2 * n) + 1)) / self.fonction_factorielle((2 * n) + 1)))
        return v

    def r(self, n):
        """
        Suite (r(n))_n
        :param n: entier naturel representant l'indice n de la suite (r(n))_n
        :return: r(:param n)
        """
        return self.fonction_sinusTaylorien(self.val, n)

    def conv(self, k):
        """
        Certificat de convergence de la suite (r(n))_n
        :param k: entier naturel representant l'ordre k du calcul du certificat de convergence conv(k)
        :return: conv(:param k)
        """
        n = 0
        ordre = 1 / (10 ** (k))
        while True:
            n += 1
            serie_approchee = (2 ** (n + 1)) / self.fonction_factorielle(n + 1)
            if (serie_approchee <= ordre):
                break
        return n

    def fonction_preuveParCauchy(self, epsilon):
        """
        Fonction prouvant la stabilite d'un developpement limité de pre 10 ** -:param epsilon
        :param epsilon: Ordre de pre souhaite du developpement limite
        :return: L'ordre du developpement limite a partir duquel :param val est stable avec une pre(ordre)
                10 ** -:param epsilon
        """
        n = 1
        while True:
            difference_de_cauchy = self.fonction_sinusTaylorien(self.val, n) - self.fonction_sinusTaylorien(self.val, n + 1)
            n += 1
            if (self.absolu(difference_de_cauchy) < epsilon):
                break
        return n - 1


# Instance de la classe PRINCIPALE  classe_General
valeur = classe_General(8 / 5)
                                               # PROGRAMME PRINCIPAL
                                               
                                               
                                               
if __name__ == '__main__':
    # Affichage des resultats attendus
                                #debut du programme 
    print('___________________[ DEBUT DU PRROGRAMME  ]___________________\n')

    resultat = valeur.conv(8)
    print(f"resultat = {resultat}")

    for i in range(0, resultat+1):
        print(f"r({i}) = {valeur.r(i)}")

    epsilon = 10 ** -6
    print(f"[INFO] Certification d'ordre {epsilon} atteinte à partir de r({valeur.fonction_preuveParCauchy(epsilon)})")

    a = valeur.fonction_tronque(valeur.r(valeur.fonction_preuveParCauchy(epsilon)), 6)
    print('a = ', a)

    print('\n__________________[ FIN  DU PROGRAMME ]__________________\n')