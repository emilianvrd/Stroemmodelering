import numpy as np
import matplotlib.pyplot as plt

land = input("Hvilket land: ")

stromtilgang_land = []


def invalid_numbers(y, reached_max):
    print("Fish")
    for i in range(len(y)):
        if y[i] > 100:
            y[i] = 100
            reached_max = True
        elif y[i] < 0:
            y[i] = 0
    if reached_max == True:
        if y[i] < 100:
            y[i] = 100


class Regresjonsanalyse:
    def __init__(self, name, stromtilgang, grad, color):
        ar_etter_2000 = []
        reached_max = False
        self.stromtilgang = stromtilgang
        x = np.linspace(0, 40, 1000)
        if len(stromtilgang) == 0:
            for i in range(0, 24, 3):
                ar_etter_2000.append(i)
                print("Hvor mange prosent hadde strøm i år", 2000 + i, ":")
                stromtilgang.append(float(input("Svar: ")))
        elif len(stromtilgang) == 22:
            for i in range(22):
                ar_etter_2000.append(i)
        if grad == 1:
            a, b = np.polyfit(ar_etter_2000, self.stromtilgang, grad)
            y = a * x + b
        elif grad == 2:
            a, b, c = np.polyfit(ar_etter_2000, self.stromtilgang, grad)
            y = a * x**2 + b * x + c
        elif grad == 3:
            a, b, c, d = np.polyfit(ar_etter_2000, self.stromtilgang, grad)
            y = a * (x**3) + b * (x**2) + c * x + d
        else:
            print(
                "Sorry, Vi klarte ikke å lage en graf som passer med kriteriene du oppga. Programmet fungerer bare opp til tredjegradsfunksjoner foreløpig"  # noqa: E501
            )
        invalid_numbers(y, reached_max)
        plt.plot(x, y, label=name, color=color)


gjennomsnitt_i_verden = Regresjonsanalyse(
    "Gjennomsnitt i verden",
    [
        78.4,
        78.8,
        79.2,
        80.1,
        80.1,
        80.8,
        81.5,
        82.1,
        82.8,
        83.0,
        83.6,
        84.6,
        85.1,
        85.8,
        86.3,
        87.0,
        88.2,
        89.0,
        89.9,
        90.2,
        90.5,
        91.4,
    ],
    3,
    "blue",
)

Kenya = Regresjonsanalyse(
    "Kenya",
    [
        15.2,
        17,
        18.9,
        16,
        22.6,
        24.5,
        26.4,
        28.3,
        30.2,
        23,
        19.2,
        36.2,
        38.1,
        40.1,
        36,
        41.6,
        53.1,
        55.8,
        61.2,
        69.7,
        71.5,
        76.5,
    ],
    2,
    "yellow",
)

land_graf = Regresjonsanalyse(land, [], 2, "red")

plt.legend()
plt.show()
