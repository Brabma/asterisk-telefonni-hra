# Telefonní hra na Asterisku

Krátká česká hra, na kterou se dá zavolat z běžného telefonu. Dovoláte se na firemní linku, jejíž automat nechce být vypnutý. Běží na Asterisku, open-source telefonní ústředně, na mém serveru s Ubuntu.

Děj a texty hry vytvořila AI. Hra je jen ukázka. Mou prací je telefonní zapojení, Asterisk a provoz serveru.

## Jak si zahrát

1. Zavolejte na **222 765 757**. Je to běžné pražské číslo, ne placená linka. Hra si nic neúčtuje, zaplatíte jen obyčejný hovor podle svého tarifu.
2. Vybírejte tlačítky **1** a **2**, klidně i během hlášky.
3. Na konci se hovor sám ukončí. Hra má pět konců, pro jiný zavolejte znovu.

Začátek hry:

> Dobrý den, dovolali jste se do firmy Kancl. Pro technickou podporu stiskněte jedna. Pro spojení se správcem stiskněte dvě.

## Jak to funguje

```text
Váš telefon → operátor Odorik → SIP → Asterisk na serveru → hra
```

- **SIP trunk** k operátorovi Odorik přes PJSIP, aby hovor došel na server a byl slyšet zvuk.
- **[Dialplan](asterisk/extensions_telefonni_adventura.conf)**, tedy pravidla, co Asterisk s hovorem dělá: přehraje hlášku a podle stisknutého tlačítka (DTMF) přejde na další scénu. Vytváří se automaticky ze [scénáře](game/SCENAR.md).
- **Server**: přístup přes SSH s klíči, firewall povolený jen pro operátora, nasazení se zálohou a pravidelná kontrola služby.
- **Diagnostika**: registrace u operátora, SIP zprávy, logy a záznamy hovorů. Podrobně v [technickém návodu](docs/TECHNICAL.md).
