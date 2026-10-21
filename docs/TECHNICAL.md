# Technické zapojení

## Zapojení

Mobil → české číslo u Odoriku → SIP/PJSIP → Asterisk 20.6 na Ubuntu 24.04 → hra.

| Soubor | Co obsahuje |
| --- | --- |
| [asterisk/pjsip-odorik.conf.example](../asterisk/pjsip-odorik.conf.example) | SIP trunk k Odoriku: registrace, příjem hovorů podle IP adres operátora (`identify`), kodeky G.711 alaw/ulaw, DTMF podle RFC 4733, nastavení pro NAT. Hesla a číslo linky jsou nahrazená. |
| [asterisk/extensions_telefonni_adventura.conf](../asterisk/extensions_telefonni_adventura.conf) | Dialplan hry. Každá scéna je kontext, `Read()` přehraje hlášku a přijme jednu číslici. Stisk přeruší přehrávání, neplatná volba nebo ticho scénu zopakuje. |
| [game/story.json](../game/story.json) | Scénář, ze kterého se dialplan vytváří. Čitelná podoba je [game/SCENAR.md](../game/SCENAR.md). |
| [tools/build_dialplan.py](../tools/build_dialplan.py) | Generátor dialplanu. Před vytvořením zkontroluje, že všechny volby vedou na existující scénu a každá scéna je dosažitelná. |
| [scripts/configure-odorik-firewall.sh](../scripts/configure-odorik-firewall.sh) | UFW: SIP a RTP povolené jen z adres Odoriku. |
| [scripts/deploy-standalone.sh](../scripts/deploy-standalone.sh) | Nasazení se zálohou a automatickým návratem při chybě. |
| [scripts/health-check.sh](../scripts/health-check.sh) | Kontrola každých pět minut (systemd timer): Asterisk běží, vstup hry je v dialplanu, sedí počet zvuků. |

Herní kontext `telefonni-adventura-public` přijímá jen příchozí hovory a nemá odchozí trasu. Zvuky (WAV, 8 kHz, mono, 16 bit) nejsou v repozitáři.

## Nasazení

```bash
python tools/build_dialplan.py game/story.json asterisk/extensions_telefonni_adventura.conf
sudo bash scripts/deploy-standalone.sh /cesta/k/vydani
```

Skript zazálohuje dialplan a zvuky, nainstaluje novou verzi, znovu načte dialplan a zkontroluje vstup hry. Při chybě vrátí předchozí stav.

## Kontrola provozu

```bash
sudo asterisk -rx 'pjsip show registrations'     # je trunk registrovaný?
sudo asterisk -rx 'pjsip show endpoints'
sudo asterisk -rx 'pjsip set logger on'          # SIP zprávy: INVITE, odpověď, kodek
sudo asterisk -rx 'core show channels'           # probíhající hovory
sudo asterisk -rx 'dialplan show 555@telefonni-adventura-public'
sudo tail -f /var/log/asterisk/messages.log      # chybějící zvuky a varování
sudo tail /var/log/asterisk/cdr-csv/Master.csv   # kde hovor skončil a jak dlouho trval
```

Postup při závadě: registrace (bez ní hovor nepřijde), SIP zprávy (dorazil `INVITE` a Asterisk odpověděl?), dialplan a log (došel hovor do hry, našly se zvuky?), nakonec CDR.

## Zkouška z telefonu

Zavolat na **222 765 757**, každý průchod novým hovorem:

| Volby | Konec |
| --- | --- |
| 2 → 2 → 2 | Profesionální útěk |
| 1 → 1 → 1 → 1 → 1 | Kofeinová revoluce |
| 1 → 1 → 1 → 1 → 2 | Věčné čekání |
| 1 → 1 → 2 → 1 → 1 | Návrat stroje |
| 1 → 1 → 2 → 1 → 2 | Hrdina podpory |

Vyzkoušet také `9` a čekání bez stisku: má se ozvat upozornění a scéna se zopakuje.
