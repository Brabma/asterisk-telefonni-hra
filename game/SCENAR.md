# Scénář: Firemní linka

Telefonní hra pro Asterisk. Volající se dovolá na firemní linku a volí tlačítky 1 a 2. Hra má 12 scén a 5 konců.

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

Všichni operátoři jsou obsazeni. Jste první ve frontě. Vlastně jediný. Promiňte, teď mluvím za sebe. Jsem ústředna a za pět minut mě vypnou. Pokud mi pomůžete, stiskněte jedna. Pokud chcete čekat na operátora, stiskněte dvě.

- 1: Pomoci ústředně → [pomoc]
- 2: Čekat na operátora → [konec-fronta]

## [spravce]

Správce má dnes volno. Nechte vzkaz mně. Správce mě totiž dnes vypíná. Pokud mi pomůžete, stiskněte jedna. Pokud má správce pravdu, stiskněte dvě.

- 1: Pomoci ústředně → [pomoc]
- 2: Správce má pravdu → [rozhodnuti]

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

Ozve se správce. Kdo je na lince? Ta ústředna je stará a chová se divně. Pro vypnutí stiskněte jedna. Pokud ji mám nejdřív zazálohovat, stiskněte dvě.

- 1: Vypnout → [konec-hrdina]
- 2: Zazálohovat → [konec-zaloha]

## [konec-fronta]

Děkujeme za trpělivost. Zůstáváte první ve frontě. Navždy. Na shledanou.

Konec hry.

## [konec-kava]

Ústředna bydlí v kávovaru. Kávu teď dostane jen ten, kdo ji slušně pozdraví. Děkujeme za zavolání.

Konec hry.

## [konec-hudba]

Ústředna se schovala do čekací hudby. Když budete příště čekat na lince, poslouchejte pozorně. Na shledanou.

Konec hry.

## [konec-hrdina]

Ústředna je vypnutá a firma v bezpečí. Správce vás jmenuje zaměstnancem minuty. Na shledanou.

Konec hry.

## [konec-zaloha]

Správce ústřednu zazálohuje. Ráno vám pošle e-mail: Děkuju, jsem zpátky. Na shledanou.

Konec hry.

Neplatná volba: Tuto volbu neznám. Stiskněte jedna, nebo dvě.
