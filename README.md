# Telefonní hra na Asterisku

Na tuhle krátkou hru se dá zavolat z běžného telefonu. Ozve se firemní ústředna, kterou chce správce vypnout. Tlačítky 1 a 2 rozhodujete, jak příběh dopadne. Hra má čtyři konce a zabere přibližně minutu.

## Jak si zahrát

1. Zavolejte na **222 765 757**.
2. Poslouchejte a vybírejte tlačítky **1** a **2** na číselníku telefonu.
3. Po dohrání se hovor sám ukončí. Pro jiný konec zavolejte znovu.

Stačí běžný mobil, žádná aplikace ani registrace. Volit lze i během hlášky.

## Jak to funguje

Hovor přijme operátor Odorik a předá ho přes SIP do Asterisku na mém serveru s Ubuntu. Asterisk přehrává nahrávky a podle stisknutých tlačítek pouští další část příběhu.

```text
Váš telefon → Odorik → Asterisk na serveru → hra
```

## Co na projektu spravuji

- **Připojení k operátorovi přes SIP/PJSIP** — aby se volající dovolal na server a slyšel zvuk.
- **Pravidla hovoru a volby tlačítky** — Asterisk podle DTMF přechází mezi scénami. Pravidla se vytvářejí z českého scénáře.
- **Linuxový server** — přístup přes SSH, firewall omezený na operátora, nasazení se zálohou a pravidelné kontroly služby.
- **Kontrolu hovorů** — registraci k operátorovi, SIP zprávy, přehrávání zvuku a záznamy o průchodu hovoru.

## Co je v repozitáři

- [Scénář hry](game/SCENAR.md) a [jeho podoba pro generátor](game/story.json).
- [Technické zapojení a diagnostika](docs/TECHNICAL.md), včetně nasazení, testování a příkazů pro Asterisk.
- [Výsledky automatických kontrol](https://github.com/Brabma/asterisk-telefonni-hra/actions).

Přihlašovací údaje a zvukové soubory nejsou veřejné. Postup vytvoření zvuků je v technickém návodu.
