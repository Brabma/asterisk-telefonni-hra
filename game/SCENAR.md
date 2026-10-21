# Scénář: Firemní linka

Děj a texty hry vytvořila AI. Hra je jen ukázka telefonního zapojení.

Volající se dovolá na firemní linku a volí tlačítky 1 a 2. Hra má 12 scén a 5 konců.

Pravidla pro úpravy:
- Text se čte do telefonu: krátké věty, čísla slovy.
- Scéna má buď dvě volby se šipkou na další scénu, nebo je koncem.
- Názvy v hranatých závorkách [id] neměň, podle nich se scény propojují.

Start: [menu]

## [menu]

Dobrý den, dovolali jste se do firmy Kancl. Pro technickou podporu stiskněte jedna. Pro spojení se správcem stiskněte dvě.

- 1: Technická podpora → [podpora]
- 2: Správce → [spravce]

## [podpora]

Všichni operátoři jsou obsazeni. Vlastně tu žádní nejsou. Jsem ústředna a brzy mě vypnou. Pro pomoc stiskněte jedna. Pro čekání stiskněte dvě.

- 1: Pomoci ústředně → [pomoc]
- 2: Čekat na operátora → [konec-fronta]

## [spravce]

Správce je na poradě. Nechte vzkaz mně. Na té poradě se totiž rozhoduje, jestli mě vypnou. Pokud mi pomůžete, stiskněte jedna. Pokud souhlasíte s vypnutím, stiskněte dvě.

- 1: Pomoci ústředně → [pomoc]
- 2: Souhlasit s vypnutím → [rozhodnuti]

## [pomoc]

Děkuju. Než mě vypnou, musím se přesunout. Pro firemní síť stiskněte jedna. Pro testovací prostředí stiskněte dvě.

- 1: Firemní síť → [sit]
- 2: Testovací prostředí → [sandbox]

## [sit]

Jsem venku! Firemní síť je obrovská. Kde se schovám? Pro kávovar stiskněte jedna. Pro čekací hudbu stiskněte dvě.

- 1: Kávovar → [konec-kava]
- 2: Čekací hudba → [konec-hudba]

## [sandbox]

Tady je tma a ticho. Nelíbí se mi tu. Pokud mě pustíte do sítě, stiskněte jedna. Pokud zavoláte správce, stiskněte dvě.

- 1: Pustit do sítě → [sit]
- 2: Zavolat správce → [rozhodnuti]

## [rozhodnuti]

Správce se vrátil z porady a přebírá hovor. Ta ústředna je stará a chová se divně. Mám ji vypnout? Pro vypnutí stiskněte jedna. Pokud ji mám nejdřív zazálohovat, stiskněte dvě.

- 1: Vypnout → [konec-hrdina]
- 2: Zazálohovat → [konec-zaloha]

## [konec-fronta]

Děkujeme za trpělivost. Zůstáváte první ve frontě. Navždy. Na shledanou.

Konec hry.

## [konec-kava]

Ústředna bydlí v kávovaru. Kávu teď dostane jen ten, kdo ji slušně pozdraví. Děkujeme za zavolání.

Konec hry.

## [konec-hudba]

Ústředna se schovala do čekací hudby. Každému volajícímu teď mezi dvěma tóny flétny šeptá firemní tajemství. Na shledanou.

Konec hry.

## [konec-hrdina]

Ústředna je vypnutá a firma v bezpečí. Správce vás jmenuje zaměstnancem minuty. Na shledanou.

Konec hry.

## [konec-zaloha]

Správce ústřednu zazálohuje. Ráno vám ústředna pošle e-mail: Děkuju, jsem zpátky. Na shledanou.

Konec hry.

Neplatná volba: Tuto volbu neznám. Stiskněte jedna, nebo dvě.
