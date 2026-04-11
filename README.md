# PoseDetectives

**Program za detekciju i analizu pravilnog držanja tijela u stvarnom vremenu**

![Glavna slika / Logo](./images/main.png)

Program koristi **MediaPipe Pose** za prepoznavanje ključnih točaka na tijelu (ramena, kukovi, koljena itd.), računa kutove između dijelova tijela i daje procjenu koliko je držanje pravilno. Idealno za učenike, nastavnike i sve koji puno sjede za računalom.

### ✨ Glavne značajke

- Uživo snimanje s web kamere
- Detekcija poze pomoću MediaPipe
- Računanje kutova (ramena–kukovi i kukovi–koljena)
- Prikaz postotka odstupanja od idealnog držanja
- Prebacivanje između normalnog i kolor-coded prikaza (zeleno = dobro, crveno = loše)
- Spremanje trenutne slike (Landmark.jpeg)
- Odabir bilo koje povezane kamere preko menija
- Moderno Tkinter sučelje s temama

![Screenshot sučelja](./images/screenshot1.png)
![Primjer detekcije](./images/screenshot2.png)

## 🚀 Preuzimanje i pokretanje

### 1. Najlakši način (preporučeno za testiranje)

1. Preuzmi cijeli repozitorij:
   - Klikni na **Code** → **Download ZIP**
   - ili kloniraj:
     ```bash
     git clone https://github.com/tvoje-korisnicko-ime/PoseDetectives.git
