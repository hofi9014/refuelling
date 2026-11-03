# Jak wgrać nową wersję Tankvii do Google Play

Plik do wgrania jest zawsze w folderze `C:\Users\Leszek\Desktop\PROJKETY\Refuelling\dist`
i ma nazwę `Tankvia-<wersja>-v<numer>.aab` (np. `Tankvia-1.3-v21.aab`). Wgrywaj zawsze najnowszy.
Plików `.apk` nie wgrywaj – są tylko do instalacji na własnym telefonie.

## 1. Sprawdź, czy poprzednia wersja nie jest jeszcze sprawdzana
1. Play Console → wybierz Tankvię (lewe menu, nazwa aplikacji).
2. Lewe menu → **Przegląd publikowanych zmian**.
3. Jeśli widzisz **„Zmiany w trakcie sprawdzania”** – poczekaj, nic nie wgrywaj.
   Jeśli **„Nie masz nieopublikowanych zmian”** – przejdź dalej.

## 2. Wgraj plik
1. Lewe menu → **Testuj i publikuj**.
2. W sekcji **Test zamknięty** kliknij strzałkę **→** przy **alpha**.
3. Kliknij **Utwórz nową wersję**.
4. Kliknij **Prześlij** i wybierz najnowszy plik `.aab` z folderu `dist`.
5. Nazwę wersji zostaw taką, jaką podpowie Google.
6. W **Informacjach o wersji** wpisz, co się zmieniło, w znacznikach języka:
   ```
   <pl-PL>
   Krótki opis zmian.
   </pl-PL>
   ```
   Komunikat **„Kod wersji X jest już w użyciu”** oznacza, że plik z tym numerem był już kiedyś wgrany
   (numer zostaje zajęty na zawsze, nawet po odrzuceniu wersji) – trzeba zbudować plik z wyższym numerem.
7. Kliknij **Dalej**. Ostrzeżenie o „pliku do odczytywania zaciemnionego kodu” jest normalne – zignoruj je.
   Jeśli jest **błąd** (czerwony), zatrzymaj się.
8. Kliknij **Zapisz**.

## 3. (Tylko gdy zmienił się wygląd) Podmień grafiki w sklepie
1. Lewe menu → **Zwiększaj liczbę użytkowników** → **Obecność w sklepie** → **Informacje o aplikacji**.
2. Przy **Domyślna strona aplikacji** kliknij **Edytuj domyślne informacje**.
3. W **Wspólne zasoby wizualne** usuń stare pliki i dodaj nowe z folderu
   `C:\Users\Leszek\Desktop\PROJKETY\Refuelling\store`:
   - **Ikona aplikacji:** `icon-512.png`
   - **Grafika:** `feature-graphic-pl.png`
   - **Zrzuty ekranu telefonu:** 6 plików z `screenshots\pl` (od `1-dashboard.png` do `6-costs.png`)
4. **Dalej** → **Oznacz zasoby jako utworzone lub edytowane za pomocą AI** → oznacz tylko ikonę i grafikę.
5. **Zapisz**.

## 4. Wyślij do Google
1. Lewe menu → **Przegląd publikowanych zmian**.
2. Kliknij **Wyślij zmiany do sprawdzenia** i potwierdź.
3. Po zatwierdzeniu testerzy dostaną aktualizację w Sklepie Play – nie trzeba im nic wysyłać.

## Link dla nowego testera
Testuj i publikuj → Test zamknięty → **alpha** → karta **Testerzy** → dopisz jego Gmail do listy
**Testerzy Tankvia** → **Zapisz** → na dole **Kopiuj link** i wyślij mu go.
