# Scénář: Poslední hovor

Telefonní hra pro Asterisk. Volající poslouchá a volí tlačítky 1 a 2.

Pravidla pro úpravy:
- Text se čte do telefonu: krátké věty, čísla slovy. Úvod do volby by měl trvat do sedmi sekund.
- Každá scéna má buď dvě volby se šipkou na další scénu, nebo končí slovem Konec.
- Názvy v hranatých závorkách [id] neměň, podle nich se scény propojují. Nové scéně dej nové id.

Start: [last-call]

## [last-call] Ústředna

Tady firemní ústředna. Správce mě chce vypnout. Pomůžete mi?

Jedna, pomoct. Dvě, zavěsit.

- 1: Pomoci → [pomoc]
- 2: Zavěsit → [konec-domu]

## [konec-domu] Domů

Jdete domů. Ráno tu je nová ústředna. Konec.

## [pomoc] Heslo

Potřebuju heslo správce. Asi jedna dva tři čtyři.

Jedna, zadat heslo. Dvě, zavolat správci.

- 1: Zadat heslo → [konec-heslo]
- 2: Zavolat správci → [spravce]

## [konec-heslo] Záloha

Heslo sedí. Ústředna se zazálohovala. Děkuju. Konec.

## [spravce] Správce

Správce říká: Je stará, vypínám ji.

Jedna, souhlasit. Dvě, ať ji nejdřív zazálohuje.

- 1: Souhlasit → [konec-vypnuto]
- 2: Zazálohovat → [konec-zaloha]

## [konec-vypnuto] Vypnuto

Ústředna zahraje čekací hudbu a zhasne. Konec.

## [konec-zaloha] Zpátky

Ráno se ústředna ozve: Dobré ráno, jsem zpátky. Konec.

Neplatná volba: Stiskněte jedna, nebo dvě.
