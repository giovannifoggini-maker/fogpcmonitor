# FogMonitor — by FogLabs

**Versione 1.7.0** · Dashboard desktop per Windows 10/11, con interfaccia scura, angoli morbidi, animazioni discrete e accenti verde menta.

FogMonitor raccoglie localmente metriche di sistema essenziali, senza telemetria e senza librerie esterne necessarie per eseguire la versione sorgente.

**English documentation:** see [`README-EN.md`](README-EN.md).

## Lingue / Languages

L'interfaccia è disponibile in **Italiano e English**. Usa il selettore `UI` nell'intestazione per cambiare lingua: la scelta viene salvata nelle impostazioni utente e mantenuta all'avvio successivo.

The interface is available in **Italian and English**. Use the `UI` selector in the header to change language. Your choice is saved in the per-user settings and restored on the next launch.

## Dashboard

- **CPU:** utilizzo complessivo, mini-grafico e cronologia fino agli ultimi 60 campioni.
- **RAM:** percentuale utilizzata, totale, usata e disponibile.
- **GPU:** uso dei motori GPU quando il contatore è disponibile in Windows; altrimenti mostra `N/D`.
- **Disco di sistema:** percentuale occupata, spazio libero e unità monitorata.
- **Processi:** ordinamento per nome, PID o RAM; filtro per nome/PID; doppio clic per copiare un PID.
- **Grafici più fluidi:** le curve statiche si ridisegnano quando arrivano nuovi dati; le animazioni muovono soltanto piccoli indicatori, riducendo il lavoro della UI.
- **Barre morbide:** transizioni temporizzate e indipendenti dalla frequenza di aggiornamento del sistema.
- **Finestra adattiva:** dimensioni iniziali calcolate in base al monitor, per usare meglio anche i display da portatile.
- **Controlli:** pausa/ripresa, aggiornamento manuale, intervallo da 1/2/5 secondi ed esportazione CSV.
- **Branding:** icona FogLabs in PNG, SVG e ICO, nome `FogMonitor` e firma `by FogLabs`.
- **Bilingue:** selettore Italiano/English con preferenza salvata localmente.

## Avvio da sorgente

Requisiti: **Windows 10/11** e Python **3.10–3.13 con Tkinter**. Per la normale esecuzione non servono pacchetti `pip` esterni.

1. Estrai tutto lo ZIP.
2. Fai doppio clic su `Avvia-FogMonitor.bat`.
3. Se non si apre, esegui `Diagnostica-FogMonitor.bat` e conserva il messaggio riportato.

In alternativa, da un terminale nella cartella del progetto:

```bat
py -3.13 FogMonitor.py
```

Gli eventuali errori si trovano in:

```text
%LOCALAPPDATA%\FogLabs\FogMonitor\FogMonitor-error.log
```

## Creare la versione EXE portabile

Lo ZIP sorgente non include un `.exe` precompilato. Per costruire l'eseguibile Windows:

1. Su Windows, installa Python 3.13 includendo Python Launcher e Tkinter.
2. Estrai il progetto in una cartella scrivibile.
3. Esegui `Build-EXE.bat`.

Lo script installa solo lo strumento di **build** PyInstaller, genera `dist\FogMonitor.exe` e crea `release\FogMonitor-by-FogLabs-Windows.zip`. Il PC destinatario non deve installare Python per usare l'EXE generato. La prima compilazione richiede una connessione Internet per scaricare PyInstaller.

## Pubblicazione tramite GitHub

È incluso `.github/workflows/windows-release.yml`. Per far generare lo ZIP Windows su GitHub:

1. Carica questa cartella in un repository GitHub.
2. Vai in **Actions** e avvia **Build Windows release**, oppure pubblica un tag che inizi con `v`, per esempio `v1.7.0`.
3. Per un'esecuzione manuale, scarica l'artefatto dalla pagina della workflow. Per un tag, la workflow allega lo ZIP alla GitHub Release.

La build Windows non è stata eseguita da questo ambiente Linux; la workflow GitHub la esegue su un runner Windows prima di creare l'artefatto.

## Accuracy, privacy and limits / Precisione, privacy e limiti

- Tutte le letture vengono elaborate localmente; non c'è login, account o invio online dei dati.
- Le API generiche utilizzate non forniscono temperature CPU/GPU affidabili: l'interfaccia non le inventa e segnala il limite.
- La disponibilità del contatore GPU dipende da Windows e dal driver grafico.
- Alcuni processi protetti potrebbero non rendere leggibili nome o memoria.
- I valori rappresentano campioni reali disponibili nel sistema; i campioni mancanti sono indicati come `N/D` o `—`.
- La cronologia CSV contiene fino a 1.800 campioni e resta in memoria durante la sessione.

## Scorciatoie

- `Ctrl + F` — ricerca processi.
- `Ctrl + R` — aggiornamento manuale.
- `Ctrl + E` — esportazione CSV.
- Doppio clic su un processo — copia PID.

## File principali

- `FogMonitor.py` — applicazione desktop.
- `Avvia-FogMonitor.bat` — avvio semplice da sorgente.
- `Diagnostica-FogMonitor.bat` — controllo di Python/Tkinter.
- `Build-EXE.bat` — crea l'eseguibile e lo ZIP Windows.
- `assets/` — loghi PNG, SVG e ICO.
- `version_info.txt` — metadati versione dell'eseguibile.
- `.github/workflows/windows-release.yml` — build e release automatizzate.
- `CHANGELOG.md` — cronologia versioni.

**Distribuzione:** il pacchetto fornito in chat è il sorgente pronto per essere caricato su GitHub. Per pubblicare un EXE firmato, occorrono una build Windows e, facoltativamente, una firma Authenticode del distributore.

## Cloudflare Pages (website)

This repository includes a static public site under `public/` for Cloudflare Pages. In Cloudflare, select **Framework preset: None**, leave Root directory blank, use **Build command: `exit 0`** (or leave it blank for static HTML), and set **Build output directory: `public`**. No environment variables are required. See [`CLOUDFLARE-PAGES.md`](CLOUDFLARE-PAGES.md) and the on-site guide at `/CLOUDFLARE-PAGES.html`.

Cloudflare Pages publishes the website and source archive only. The Windows desktop EXE is built separately on Windows or through GitHub Actions.
