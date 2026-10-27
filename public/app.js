(() => {
  const translations = {
    it: {
      navFeatures: 'Funzioni', navDownload: 'Download', eyebrow: 'MONITOR DI SISTEMA WINDOWS', heroTitle: 'Il tuo PC.<br><span class="mint">Sotto controllo.</span>',
      heroLead: 'Un monitor di sistema pulito, leggero e bilingue. Dati essenziali, controlli immediati e animazioni discrete, senza account o telemetria.',
      sourceCta: 'Scarica il pacchetto sorgente', howTo: "Come ottenere l'EXE", localData: 'Dati locali', previewLive: 'IN ESECUZIONE', previewTitle: 'Prestazioni del sistema', previewCpu: 'Utilizzo processore', previewMemory: 'Memoria in uso', previewGraphics: 'Motore grafico', previewDisk: 'Unità di sistema', previewLocal: 'Campionamento locale',
      builtFor: 'PROGETTATO PER IL DESKTOP', featuresTitle: 'Tutto ciò che serve.<br><span class="muted">Niente rumore.</span>', featureCpu: 'Controlla utilizzo del processore, memoria disponibile e andamento recente.', featureGpuTitle: 'GPU & disco', featureGpu: 'Legge i contatori disponibili in Windows e indica chiaramente quando un dato non è supportato.', featureProcessTitle: 'Processi chiari', featureProcess: 'Cerca e ordina i processi, copia i PID ed esporta la cronologia in CSV.', featurePrivacyTitle: 'Privacy locale', featurePrivacy: 'Nessun account e nessuna telemetria: le letture vengono elaborate sul PC.', getStarted: 'PER INIZIARE', downloadTitle: 'Pronto per Windows.', downloadLead: 'Questa pagina è il portale statico di FogMonitor. Cloudflare Pages ospita il sito e il pacchetto sorgente; la compilazione dell\'app desktop Windows viene eseguita separatamente.', sourcePackage: 'Pacchetto sorgente · IT / EN', downloadSource: 'Scarica i sorgenti', sourceNotice: "Per ottenere FogMonitor.exe, esegui Build-EXE.bat su Windows oppure avvia la GitHub Action Windows release.", buildTitle: 'Vuoi il file .exe?', buildText: 'Cloudflare Pages non compila né esegue applicazioni desktop Python. Usa la build Windows inclusa in GitHub Actions per creare lo ZIP portabile dell’app.', deployGuide: 'Guida Cloudflare →', footerLine: 'Creato con cura per Windows · v1.7.0', deploySettings: 'Impostazioni di pubblicazione'
    },
    en: {
      navFeatures: 'Features', navDownload: 'Download', eyebrow: 'WINDOWS SYSTEM MONITOR', heroTitle: 'Your PC.<br><span class="mint">In clear view.</span>',
      heroLead: 'A clean, lightweight, bilingual system monitor. Essential metrics, quick controls and subtle animations — with no account or telemetry.',
      sourceCta: 'Download source package', howTo: 'How to get the EXE', localData: 'Local data', previewLive: 'RUNNING', previewTitle: 'System performance', previewCpu: 'Processor usage', previewMemory: 'Memory in use', previewGraphics: 'Graphics engine', previewDisk: 'System drive', previewLocal: 'Local sampling',
      builtFor: 'MADE FOR YOUR DESKTOP', featuresTitle: 'Everything you need.<br><span class="muted">Nothing you don’t.</span>', featureCpu: 'Check processor usage, available memory and recent activity.', featureGpuTitle: 'GPU & storage', featureGpu: 'Reads counters available in Windows and clearly marks unsupported metrics.', featureProcessTitle: 'Clear process list', featureProcess: 'Search and sort processes, copy PIDs and export history to CSV.', featurePrivacyTitle: 'Local privacy', featurePrivacy: 'No account and no telemetry: readings are processed on your PC.', getStarted: 'GET STARTED', downloadTitle: 'Ready for Windows.', downloadLead: 'This page is FogMonitor’s static website. Cloudflare Pages hosts the site and source package; the Windows desktop app is built separately.', sourcePackage: 'Source package · IT / EN', downloadSource: 'Download source', sourceNotice: 'To create FogMonitor.exe, run Build-EXE.bat on Windows or start the Windows release GitHub Action.', buildTitle: 'Need the .exe?', buildText: 'Cloudflare Pages does not compile or run Python desktop applications. Use the Windows build in GitHub Actions to create the portable app ZIP.', deployGuide: 'Cloudflare guide →', footerLine: 'Made with care for Windows · v1.7.0', deploySettings: 'Deployment settings'
    }
  };
  const toggle = document.getElementById('langToggle');
  let language = 'it';
  try { language = localStorage.getItem('fogmonitor-site-language') === 'en' ? 'en' : 'it'; } catch (_) {}
  function setLanguage(next) {
    language = translations[next] ? next : 'it';
    document.documentElement.lang = language;
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.dataset.i18n;
      if (translations[language][key]) el.textContent = translations[language][key];
    });
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
      const key = el.dataset.i18nHtml;
      if (translations[language][key]) el.innerHTML = translations[language][key];
    });
    toggle.textContent = language === 'it' ? 'EN' : 'IT';
    toggle.setAttribute('aria-label', language === 'it' ? 'Switch to English' : 'Passa all’italiano');
    try { localStorage.setItem('fogmonitor-site-language', language); } catch (_) {}
  }
  toggle.addEventListener('click', () => setLanguage(language === 'it' ? 'en' : 'it'));
  setLanguage(language);
})();
