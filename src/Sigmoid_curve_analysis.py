# %%Sigmoide curve
import matplotlib.pyplot as plt
import numpy as np

# %%Leser fila

file = "/Users/synnoveronnekleiv/Downloads/test_1.txt"  # Definerer hvilke fil som leses

liste = []  # lager en tom liste (skal inneholde punktene)
x = []  # tom liste, skal inneholde x-verdiene til sigmoidkurva
y = []  # tom liste, skal inneholde y-verdiene til sigmoidkurva

with open(file, 'r') as infile:  # Åpner fila i lesemodus, fila lukkes automatisk
    lines = infile.readlines()  # leser alle linjene og lagrer de
    for line in lines:  # Skal gå gjennom alle linjene en for en
        words = line.split()  # Splitter på mellomrom, for å skille x og y-verdiene
        if len(words) < 2:  # Sjekker om words inneholder mindre enn to elementer
            continue  # Hvis den inneholder mindre enn to skjer ingen ting
        else:  # Hvis ikke går den videre
            liste.append(words)  # Appender x og y verdi i en felles liste
            a = words[0].strip(" ")  # Fjerner eventuelle mellomrom fra x-verdiene
            b = words[1].strip(" ")  # Fjerner eventuelle mellomrom fra y-verdiene
            x.append(float(a))  # Legger x-verdiene i egen liste
            y.append(float(b))  # Legger y verdien i egen liste

# %% 1) Lage baselines
toppunkt = max(y)  # Finner toppunkt, det øvre platået
bunnpunkt = min(y)  # Finner bunnpunktet, det nedre platået

# %% 2) Finne gjennomsnittet av baselinene
gjennomsnitt = (toppunkt - bunnpunkt) / 2  # Finner halveringspunktet (y-verdien)

# %% 3) Whileløkke som kjører så lenge
# <(c-k)/2 øker x  med 1 til å begynne
# med, erstatte med lavere tall etterhvert

y_nr = 0

while y[y_nr] > gjennomsnitt:  # Løper gjennom lista frem til vi kommer til en verdi
    # som er mindre enn halveringspunktet
    y_nr += 1  # Opptarer y-indeksen, ønsker å vite plasseringen til verdien i y-lista

# Estimert x-verdi for halveringspunktet
x_ukjent = x[y_nr]  # Henter ut x-verdien som hører sammen med y-verdien, står på samme plass
x_ukjentpluss1 = x[y_nr + 1]  # Henter ut verdien etter vår x-verdi
x_endelig = (x_ukjentpluss1 + ((x_ukjent - x_ukjentpluss1) / 2))  # Regner midtpunktet mellom
# x-verdiene for å få en mer nøyaktig verdi
print("x-value for c/2:", x_endelig)

# Estimert y-verdi for halveringspunktet
y_ukjent = y[y_nr]  # Henter ut x-verdien som hører sammen med y-verdien, står på samme plass
y_ukjentpluss1 = y[y_nr + 1]  # Henter ut verdien etter vår x-verdi
y_endelig = (y_ukjentpluss1 + ((y_ukjent - y_ukjentpluss1) / 2))  # Regner midtpunktet mellom
# x-verdiene for å få en mer nøyaktig verdi
print("y-value for c/2:", y_endelig)

# %% 4) Finn tangenten i dette punktet

# y2-y1=a*(x2-x1)
# y=ax+b

# Definerer punktene, veldig små tall så trenger litt større intervall
x1 = x[y_nr - 5]
x2 = x[y_nr + 5]
y1 = y[y_nr - 5]
y2 = y[y_nr + 5]

x_tangent = np.linspace(x_endelig - 75, x_endelig + 75, int(150 / 0.03))  # Definerer x-verdier for tangenten

stigningstall = (y2 - y1) / (x2 - x1)  # Regner ut stigningstallet

konstantledd = -stigningstall * x_endelig + y_endelig  # Regner ut konstantleddet

y_tangent = [stigningstall * x_tg + konstantledd for x_tg in x_tangent]

print("formula for tangent: y =", stigningstall, "* x +", konstantledd)

# %% 5) While-løkke som kjører så lenge toppunkt > tangent
y_tg = 0

while y_tangent[y_tg] > toppunkt:  # Løper gjennom lista frem til vi kommer til en verdi
    # som er mindre enn halveringspunktet
    y_tg += 1  # Opptarer y-indeksen, ønsker å vite plasseringen til verdien i y-lista

# Estimert x-verdi for skjæring med øvre baseline
x_ukjent_tg = x_tangent[y_tg]  # Henter ut x-verdien som hører sammen med y-verdien, står på samme plass
x_ukjentpluss1_tg = x_tangent[y_tg + 1]  # Henter ut verdien etter vår x-verdi
x_endelig_tg = (x_ukjentpluss1_tg + ((x_ukjent_tg - x_ukjentpluss1_tg) / 2))  # Regner midtpunktet mellom
# x-verdiene for å få en mer nøyaktig verdi
print("x-value for legphase:", x_endelig_tg)

# Estimert y-verdi for skjæring med øvre baseline
y_ukjent_tg = y_tangent[y_tg]  # Henter ut x-verdien som hører sammen med y-verdien, står på samme plass
y_ukjentpluss1_tg = y_tangent[y_tg + 1]  # Henter ut verdien etter vår x-verdi
y_endelig_tg = (y_ukjentpluss1_tg + ((y_ukjent_tg - y_ukjentpluss1_tg) / 2))  # Regner midtpunktet mellom
# x-verdiene for å få en mer nøyaktig verdi
print("y-value for legphase:", y_endelig_tg)

# %%Plotte
plt.plot(x, y)  # Plotter sigmoidkurven
plt.plot(x_endelig, y_endelig, "gX")  # Plotter c/2
plt.plot(x_tangent, (stigningstall * x_tangent + konstantledd), "k-")  # Plotter tangenten til punktet
plt.plot(x_endelig_tg, y_endelig_tg, "bX")  # Plotter halveringspunktet
plt.axhline(toppunkt, color='r', linestyle='-')  # Plotter assymptoten til toppunktet
plt.axhline(bunnpunkt, color='r', linestyle='-')  # Plotter assymptotene til bunnpunktet
plt.axhline(gjennomsnitt, color='r', linestyle='--')  # Plotter assymptotene til bunnpunktet

plt.xticks(np.arange(min(x), max(x) + 1, 30))  # Definerer verdiene på x-aksen, har intervaller på 50
plt.yticks(np.arange(min(y_tangent), max(y_tangent) + 1, 20))  # Definerer verdiene på y-aksen, har intervaller på 10
plt.title("Estimate of legphase")  # Gir plottet en tittel
plt.xlabel("Time (sec)")  # Definerer hva x-aksen viser
plt.ylabel("Concentration H2O2 (µM)")  # Definerer hva y-aksen viser
plt.legend(["Sigmoidcurve", "c/2", "Tangent", "Legphase"])  # Sier hva de ulike grafene er

plt.savefig("Cyanide affect on H2O2 consumption.png")