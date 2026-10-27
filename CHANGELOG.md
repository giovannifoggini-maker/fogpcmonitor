# Changelog — FogMonitor

## 1.7.0
- Added a complete Italian/English interface selector in the header.
- Saved the selected language in a per-user settings file and restored it at next launch.
- Localized resource labels, status indicators, tool buttons, process table, update intervals, export dialogs and empty/error states.
- Rebuilt the UI when switching language while preserving the current sample history and monitoring interval.
- Documented bilingual behavior in Italian and English.

## 1.6.0
- Reso il rendering più leggero: il grafico CPU e le mini-curve non vengono più ridisegnati ad ogni frame d'animazione.
- Animati separatamente gli indicatori luminosi delle mini-curve, aggiornando soltanto le coordinate del piccolo alone.
- Sincronizzata la velocità delle animazioni con il tempo reale invece di incrementare la fase a ogni callback.
- Rese più morbide le transizioni delle barre con easing basato su tempo.
- Aggiornata la tabella processi in-place per evitare lampeggi e ridurre la perdita di selezione durante l'aggiornamento.
- Adattata la dimensione iniziale della finestra al monitor, con un layout compatto per display di portatili e una dashboard completa su schermi più alti.
- Spostati i log di errore in `%LOCALAPPDATA%\\FogLabs\\FogMonitor` per supportare cartelle d'installazione non scrivibili e la build EXE.
- Preparati `Build-EXE.bat`, icona `.ico`, metadati versione e dipendenza di build PyInstaller.
- Aggiunta la GitHub Actions workflow per compilare su Windows e pubblicare uno ZIP portabile in corrispondenza dei tag `v*`.
- Documentati chiaramente i passaggi di build e i limiti delle letture GPU/temperatura.

## 1.5.0
- Aggiornata l'identità visiva con un simbolo “F” geometrico e futuristico, orbita segmentata e pixel dati.
- Aggiornato il wordmark FogMonitor e la firma “by FogLabs”.
- Aggiunta un'icona PNG della finestra e la sorgente SVG.

## 1.4.0
- Aggiunti micro-grafici alle schede CPU, RAM, GPU e disco.
- Aggiunta animazione ambientale discreta e indicatore sull'ultimo campione CPU.

## 1.3.0
- Arrotondati pannelli, schede metriche, controlli e ricerca.
- Ammorbidite le spaziature e le scrollbar.

## 1.2.0
- Aggiornata la dashboard e aggiunte transizioni alle barre.
- Aggiunto selettore intervallo, ricerca processi, ordinamento e scorciatoie.

## 1.1.0
- Spostata la raccolta metriche in un thread separato.
- Aggiunti pausa/ripresa, aggiornamento manuale e esportazione CSV.

## 1.0.0
- Prima dashboard CPU, RAM, GPU best-effort, disco, informazioni sistema e processi.
