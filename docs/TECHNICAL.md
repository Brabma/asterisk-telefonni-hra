# Zapojení, nasazení a kontrola hry

## Zapojení

Mobil → české číslo u Odoriku → SIP/PJSIP → Asterisk 20.6 na Ubuntu 24.04 → hra.

[Konfigurace trunku](../config/pjsip-odorik.conf.example) ukazuje registraci k operátorovi, příjem hovorů podle IP adres (`identify`), kodeky G.711 alaw/ulaw a tlačítkové volby DTMF podle RFC 4733. Parametry `rtp_symmetric`, `force_rport` a `rewrite_contact` pomáhají s provozem přes NAT.

[Pravidla firewallu](../scripts/configure-odorik-firewall.sh) omezují SIP a RTP na operátora. SIP port musí odpovídat konfiguraci PJSIP; adresy operátora před použitím ověřit. SSH používá klíče. Herní kontext `telefonni-adventura-public` nemá odchozí trasu.

Každá scéna má vlastní kontext. `Read()` přehrává hlášku a přijímá jednu číslici. Platná volba přeruší přehrávání; neplatná volba nebo čekání bez stisku zopakuje scénu po upozornění.

## Příprava vydání

Příkazy se spouštějí z kořene repozitáře. [Scénář pro čtení](../game/SCENAR.md) musí odpovídat [zdrojovému JSON](../game/story.json).

```bash
python tools/build_dialplan.py game/story.json build/extensions_telefonni_adventura.conf
python -m unittest discover -s tests -v
```

Generátor zároveň kontroluje scénář a dosažitelnost všech scén. Neplatný scénář odmítne před vytvořením dialplanu.

Pro audio je potřeba Windows s českým hlasem Microsoft Jakub a Python s NumPy:

```powershell
python -m pip install -r tools/requirements.txt
python tools/generate_audio_winrt.py --rate 2
python -m unittest discover -s tests -v
```

Nástroj vytvoří `audio/`: WAV, 8 kHz, mono, 16 bitů. Ořezává ticho, zkracuje pauzy a srovnává hlasitost. Nahrávky poslechnout; test formátu nezaručuje srozumitelnost. Bez `audio/` se test zvuků přeskočí.

## Nasazení na připravený server

Předpokladem je běžící Asterisk, připojený SIP trunk, nastavený firewall a funkční přístup přes SSH. Repozitář obsahuje soubory pro hru a její provoz; příprava operačního systému se provádí samostatně.

Na server přenést `game/`, `tools/`, `scripts/` a vytvořené `audio/`. Potom spustit:

```bash
sudo bash scripts/deploy-standalone.sh /cesta/k/vydani
```

Skript vytvoří dialplan, zálohuje konfiguraci a zvuky, nainstaluje vydání a znovu načte dialplan. Následně instaluje systemd kontrolu každých pět minut. Při chybě po záloze obnoví dialplan, audio a očekávaný počet souborů; systemd jednotky a stav timeru součástí této obnovy nejsou.

Existující blok `BEGIN TELEFONNI ADVENTURA STANDALONE` v `extensions.conf` se nepřepisuje. Má směrovat na `telefonni-adventura-entry,555,1`.

## Kontrola provozu

```bash
sudo asterisk -rx 'pjsip show registrations'
sudo asterisk -rx 'pjsip show endpoints'
sudo asterisk -rx 'core show channels'
sudo asterisk -rx 'dialplan show 555@telefonni-adventura-public'
sudo bash scripts/verify-vps.sh
```

Očekává se registrovaný trunk, správný vstup hry a health check `audio_files=17/17`. Health check ověřuje službu, směrování a počet souborů; slyšitelnost ani obsah nahrávek neověřuje.

Pro podrobnou diagnostiku zapnout `sudo asterisk -rx 'pjsip set logger on'`, po skončení opět vypnout příkazem `sudo asterisk -rx 'pjsip set logger off'`. V SIP zprávách sledovat `INVITE`, odpověď a sjednaný kodek. Zvuk se přenáší samostatně přes RTP. Přechody scén a chyby audia hledat v `/var/log/asterisk/messages.log`, kontext a délku hovoru v `/var/log/asterisk/cdr-csv/Master.csv`. Přístupové údaje a úplné provozní logy nejsou veřejné.

## Zkouška z telefonu

Zavolat na **222 765 757**. Každý průchod začíná novým hovorem:

| Volby | Konec |
| --- | --- |
| 2 → 2 → 2 | Profesionální útěk |
| 1 → 1 → 1 → 1 → 1 | Kofeinová revoluce |
| 1 → 1 → 1 → 1 → 2 | Věčné čekání |
| 1 → 1 → 2 → 1 → 1 | Návrat stroje |
| 1 → 1 → 2 → 1 → 2 | Hrdina podpory |

Ke stejným koncům vedou i další cesty, například přes diagnostiku nebo zpětné volání.

Ověřit srozumitelnost, reakci na tlačítka během hlášky a zavěšení na konci. Vyzkoušet také `9` a čekání bez stisku: má se ozvat upozornění a zopakovat scéna. Dvěma současnými hovory lze samostatně ověřit oddělení průchodů; jednotkové testy tento provozní test neprovádějí.

Automatické kontroly na GitHubu ověřují scénář, generování, Python testy a shellové skripty. Na veřejné číslo nevolají.
