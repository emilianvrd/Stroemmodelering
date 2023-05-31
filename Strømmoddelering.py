import numpy as np
import matplotlib.pyplot as plt

stromtilgang_land = []
colors = [
    "red",
    "green",
    "black",
    "yellow",
    "orange",
    "pink",
    "grey",
    "violet",
    "lime",
    "purple",
]


def filter_invalid_numbers(y):
    # Vi vil ikke ekstrapolere over 100% eller under 0% eller få grafen til å synke
    for i, val in enumerate(y):
        if val > 100:
            y[i] = 100
        if val < 0:
            y[i] = 0
        if i > 0:
            if val < y[i - 1]:
                y[i] = y[i - 1]


def load_data(path):
    countries = {}
    with open(path) as f:
        count = 0
        ar = None
        for line in f:
            line = line.strip()
            if not line:
                continue

            count += 1
            print(line, count)
            if count == 3:
                data = line.split(",")
                for i in range(5):
                    data.pop(0)
                ar = [int(i.replace('"', "")) for i in data if i]
                # Det er ett år for mye
            if count > 4:
                if ar is None:
                    raise RuntimeError("Did not read heatherline")
                country = CountryData(line, ar)
                countries[country.name] = country
    return countries


class CountryData:
    def __init__(self, line, ar):
        data = line.split(",")
        self.ar = ar
        self.name = data[0].replace('"', "")
        for i in range(5):
            data.pop(0)
        self.eldata = []
        for i in data:
            i = i.replace('"', "")
            i = i.strip()
            if i:
                i = float(i)
            else:
                i = None
            self.eldata.append(i)
        self.eldata.pop(-1)

        print(len(self.eldata), len(ar))
        print(self.eldata[-4], ar[-4])

    def plot(self, name, color):
        ar = [self.ar[i] - 2000 for i in range(-24, -2)]
        eldata = [self.eldata[i] for i in range(-24, -2)]
        # filter out missing data
        ny_ar = []
        ny_eldata = []
        for idx, val in enumerate(eldata):
            if val is not None:
                ny_ar.append(ar[idx])
                ny_eldata.append(eldata[idx])

        analyse = Regresjonsanalyse(name, ny_eldata, 2)
        analyse.plot(color)
        print(ny_ar, ny_eldata)


class Regresjonsanalyse:
    def __init__(self, name, stromtilgang, grad):
        self.name = name
        self.stromtilgang = stromtilgang
        self.grad = grad

    def plot(self, color):
        ar_etter_2000 = []
        x = np.linspace(0, 40, 1000)

        for i in range(len(self.stromtilgang)):
            ar_etter_2000.append(i)
        if self.grad == 1:
            a, b = np.polyfit(ar_etter_2000, self.stromtilgang, self.grad)
            y = a * x + b
        elif self.grad == 2:
            a, b, c = np.polyfit(ar_etter_2000, self.stromtilgang, self.grad)
            y = a * x**2 + b * x + c
        elif self.grad == 3:
            a, b, c, d = np.polyfit(ar_etter_2000, self.stromtilgang, self.grad)
            y = a * (x**3) + b * (x**2) + c * x + d
        else:
            print(
                "Sorry, Vi klarte ikke å lage en graf som passer med kriteriene du oppga. Programmet fungerer bare opp til tredjegradsfunksjoner foreløpig"  # noqa: E501
            )
        filter_invalid_numbers(y)
        plt.xlabel("År etter 2000")
        plt.ylabel("% andel med strømtilgang")
        ax = plt.gca()
        # ax.set_xlim([, xmax])
        ax.set_ylim([0.0, 110])
        plt.plot(x, y, label=self.name, color=color)


def start():
    antall_land = int(input("Hvor mange land vil du plotte?"))
    if antall_land > 10:
        print("Programmet blir for kaotisk med mer enn 10 grafer")
        start()
    for i in range(antall_land):
        while True:
            name = input("Skriv et land du vil du plotte?")
            if name in countries:
                countries[name].plot(name, colors[i])
                break
            else:
                print("Finner ikke landet, prøv igen")


if __name__ == "__main__":
    countries = load_data("Data.csv")
    print(countries.keys())
    start()

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
    )
    gjennomsnitt_i_verden.plot("blue")

    plt.legend()
    plt.show()
