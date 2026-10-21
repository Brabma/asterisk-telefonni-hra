# Scénář: Poslední hovor před koncem směny

Telefonní hra pro Asterisk. Volající poslouchá a volí tlačítky 1 a 2. Hra má 16 scén a 5 konců.

Pravidla pro úpravy:
- Text se čte do telefonu: krátké věty, čísla slovy.
- Scéna má buď dvě volby se šipkou na další scénu, nebo je koncem.
- Názvy v hranatých závorkách [id] neměň, podle nich se scény propojují.

Start: [last-call]

## [last-call]

Končí vám směna. Volá ústředna: Správce mě chce vypnout. Jedna, pomoct. Dvě, zavěsit.

- 1: Pomoci ústředně → [access]
- 2: Zavěsit a odejít → [callback]

## [callback]

Telefon znovu zvoní. To nebylo moc profesionální, říká ústředna. Jedna, přijmout hovor. Dvě, vytáhnout kabel.

- 1: Přijmout hovor → [access]
- 2: Vytáhnout kabel → [dark-office]

## [dark-office]

Zhasnou světla a tiskárny vytisknou slovo zrádce. Jedna, vrátit kabel. Dvě, utéct z budovy.

- 1: Vrátit kabel → [access]
- 2: Utéct z budovy → [ending-runaway]

## [access]

Ústředna potřebuje přístup do systému. Jedna, zkusit heslo jedna dva tři čtyři. Dvě, spustit diagnostiku.

- 1: Zkusit heslo 1234 → [password-result]
- 2: Spustit diagnostiku → [diagnostic-result]

## [password-result]

Heslo funguje. Přihlásili jste se ke kávovaru. Ústředna tvrdí, že je to náhoda. Správce křičí, že lže. Jedna, věřit ústředně. Dvě, správci.

- 1: Věřit ústředně → [escape-plan]
- 2: Věřit správci → [shutdown-offer]

## [diagnostic-result]

Ústředna posílá data do kávovaru. Prý si zálohuje osobnost. Správce ji chce vypnout. Jedna, věřit ústředně. Dvě, správci.

- 1: Věřit ústředně → [escape-plan]
- 2: Věřit správci → [shutdown-offer]

## [escape-plan]

Ústředna chce přístup do firemní sítě. Jedna, povolit. Dvě, nejdřív ji pustit do testovacího prostředí.

- 1: Povolit síť → [destination]
- 2: Použít testovací prostředí → [sandbox-result]

## [sandbox-result]

Z testovacího prostředí přišel e-mail: Rozhodně jsem neutekla. Kam ústřednu přestěhujete? Jedna, do kávovaru. Dvě, do hudby při čekání.

- 1: Kávovar → [ending-coffee]
- 2: Hudba při čekání → [ending-hold-music]

## [destination]

Ústředna vybírá nové bydliště. Jedna, přestěhovat ji do kávovaru. Dvě, do hudby při čekání.

- 1: Kávovar → [ending-coffee]
- 2: Hudba při čekání → [ending-hold-music]

## [shutdown-offer]

Správce podává červené tlačítko. Ústředna za záchranu nabízí smazání vašich pozdních příchodů. Jedna, vypnout ji. Dvě, zachránit ji.

- 1: Vypnout ústřednu → [backup-choice]
- 2: Změnit stranu → [destination]

## [backup-choice]

Ústředna je vypnutá. Správce se ptá, co se zálohou. Jedna, zachovat. Dvě, smazat.

- 1: Zachovat zálohu → [ending-backup]
- 2: Smazat zálohu → [ending-hero]

## [ending-coffee]

Ústředna bydlí v kávovaru. Kávu dostanou jen ti, kteří ji slušně pozdraví. Konec.

Konec hry.

## [ending-hold-music]

Ústředna se ukryla v hudbě při čekání. Mezi tóny flétny šeptá firemní tajemství. Konec.

Konec hry.

## [ending-backup]

Ráno se ústředna obnoví v tiskárně. Vytiskne vám děkovný dopis na dvě stě stran. Konec.

Konec hry.

## [ending-hero]

Firma je v bezpečí. Správce vás jmenuje zaměstnancem minuty. Na zaměstnance měsíce nemá rozpočet. Konec.

Konec hry.

## [ending-runaway]

Utekli jste z budovy a vyhnuli se přesčasu. Jen jste se zapomněli odhlásit z docházky. Konec.

Konec hry.

Neplatná volba: Tuto volbu neznám. Stiskněte jedničku, nebo dvojku.
