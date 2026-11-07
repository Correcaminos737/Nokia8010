import { TvBridge } from './tvBridge.js';

const kodiStatusText = document.getElementById('kodi-status-text');
const kodiBadge = document.getElementById('kodi-badge');
const usbStatusText = document.getElementById('usb-status-text');
const usbPathSpan = document.getElementById('usb-path');
const usbSpaceSpan = document.getElementById('usb-space');
const storageBadge = document.getElementById('storage-perm-badge');
const logMessage = document.getElementById('log-message');

const retroarchBadge = document.getElementById('retroarch-status-badge');
const btnInstallRetroarch = document.getElementById('btn-install-retroarch');
const btnLaunchRetroarch = document.getElementById('btn-launch-retroarch');
const retroProgressContainer = document.getElementById('retroarch-progress-container');
const retroProgressBar = document.getElementById('retroarch-progress-bar');
const retroProgressText = document.getElementById('retroarch-progress-text');

const btnDownloadRoms = document.getElementById('btn-download-roms');
const btnLaunchRom = document.getElementById('btn-launch-rom');
const selectArcadeGame = document.getElementById('select-arcade-game');
const customRomUrl = document.getElementById('custom-rom-url');
const romsProgressContainer = document.getElementById('roms-progress-container');
const romsProgressBar = document.getElementById('roms-progress-bar');
const romsProgressText = document.getElementById('roms-progress-text');

let detectedUsbPath = null;
let lastDownloadedRomPath = null;

// Catálogo de ROMs Arcade FBNeo / BIOS
const ARCADE_DATABASE = {
  neogeo: {
    fileName: 'neogeo.zip',
    url: 'https://raw.githubusercontent.com/libretro/fbneo/master/metadata/neogeo.zip' // fallback / mirror
  },
  bublbobl: {
    fileName: 'bublbobl.zip',
    url: 'https://archive.org/download/fbneo_1003_bestset/bublbobl.zip'
  },
  sf2: {
    fileName: 'sf2.zip',
    url: 'https://archive.org/download/fbneo_1003_bestset/sf2.zip'
  }
};

selectArcadeGame.addEventListener('change', () => {
  if (selectArcadeGame.value === 'custom') {
    customRomUrl.style.display = 'block';
  } else {
    customRomUrl.style.display = 'none';
  }
});

function setLog(msg) {
  console.log('[TV Log]', msg);
  if (logMessage) logMessage.textContent = msg;
}

// Formatear bytes
function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// 1. Comprobar permisos
async function checkPermissions() {
  try {
    const status = await TvBridge.checkPermissionsStatus();
    if (status.hasStorageAccess) {
      storageBadge.textContent = 'Almacenamiento: Autorizado';
      storageBadge.className = 'badge badge-success';
    } else {
      storageBadge.textContent = 'Almacenamiento: Requiere Permiso';
      storageBadge.className = 'badge badge-warning';
      storageBadge.onclick = () => TvBridge.requestStoragePermission();
    }
  } catch (err) {
    setLog('Error comprobando permisos: ' + err.message);
  }
}

// 2. Comprobar si Kodi está presente
async function checkKodi() {
  try {
    setLog('Verificando presencia de Kodi...');
    const res = await TvBridge.checkKodiPackage();
    if (res.installed) {
      kodiStatusText.textContent = `Instalado (Versión: ${res.versionName || 'Detectada'})`;
      kodiBadge.textContent = 'PRESENTE';
      kodiBadge.className = 'badge badge-success';
      setLog(`Kodi detectado con éxito: ${res.packageName}`);
    } else {
      kodiStatusText.textContent = 'No instalado en el sistema.';
      kodiBadge.textContent = 'NO ENCONTRADO';
      kodiBadge.className = 'badge badge-neutral';
    }
  } catch (e) {
    setLog('Error al consultar Kodi: ' + e.message);
  }
}

// 3. Comprobar RetroArch
async function checkRetroArch() {
  try {
    const res = await TvBridge.checkRetroArchPackage();
    if (res.installed) {
      retroarchBadge.textContent = 'INSTALADO';
      retroarchBadge.className = 'badge badge-success';
      btnLaunchRetroarch.style.display = 'inline-block';
    } else {
      retroarchBadge.textContent = 'NO INSTALADO';
      retroarchBadge.className = 'badge badge-neutral';
      btnLaunchRetroarch.style.display = 'none';
    }
  } catch (e) {
    console.error(e);
  }
}

// 4. Identificar dinámicamente el pendrive USB
async function checkUsbStorage() {
  try {
    setLog('Escaneando volúmenes de almacenamiento externo...');
    const res = await TvBridge.getUsbStorage();
    if (res.detected && res.mountPath) {
      detectedUsbPath = res.mountPath;
      usbStatusText.textContent = `Pendrive Conectado (${res.uuid || 'USB'})`;
      usbPathSpan.textContent = `Ruta: ${res.mountPath}`;
      usbSpaceSpan.textContent = `Libre: ${formatBytes(res.freeSpaceBytes)}`;
      setLog(`USB detectado en: ${res.mountPath} (${formatBytes(res.freeSpaceBytes)} libres)`);
    } else {
      usbStatusText.textContent = 'No se detecta pendrive USB externo.';
      usbPathSpan.textContent = 'Ruta: Ninguna';
      usbSpaceSpan.textContent = 'Libre: --';
      setLog('No se encontró ningún volumen USB extraíble en /storage/');
    }
  } catch (e) {
    setLog('Error detectando USB: ' + e.message);
  }
}

// 5. Escuchar eventos de progreso nativo
TvBridge.addListener('downloadProgress', (data) => {
  if (data.type === 'retroarch') {
    retroProgressContainer.style.display = 'block';
    retroProgressBar.style.width = `${data.percent}%`;
    retroProgressText.textContent = `Descargando APK: ${data.percent}% (${formatBytes(data.downloaded)} / ${formatBytes(data.total)})`;
  } else if (data.type === 'roms') {
    romsProgressContainer.style.display = 'block';
    romsProgressBar.style.width = `${data.percent}%`;
    romsProgressText.textContent = `Descargando ${data.fileName || 'ROM'}: ${data.percent}% (${formatBytes(data.downloaded)} / ${formatBytes(data.total)})`;
  }
});

// Eventos de botones
btnInstallRetroarch.addEventListener('click', async () => {
  try {
    setLog('Iniciando descarga de RetroArch (armeabi-v7a) en caché...');
    btnInstallRetroarch.disabled = true;
    retroProgressContainer.style.display = 'block';
    retroProgressBar.style.width = '0%';
    retroProgressText.textContent = 'Conectando con servidor...';

    // URL oficial de RetroArch para Android v7a
    const apkUrl = 'https://buildbot.libretro.com/stable/1.19.1/android/RetroArch.apk';
    const res = await TvBridge.downloadAndInstallApk({ url: apkUrl });

    setLog('Intent de instalación lanzado. Por favor confirme con el mando de la TV.');
    setTimeout(checkRetroArch, 10000);
  } catch (err) {
    setLog('Fallo instalando RetroArch: ' + err.message);
  } finally {
    btnInstallRetroarch.disabled = false;
  }
});

btnLaunchRetroarch.addEventListener('click', async () => {
  try {
    setLog('Iniciando RetroArch...');
    await TvBridge.launchRetroArch({});
  } catch (err) {
    setLog('Error al lanzar RetroArch: ' + err.message);
  }
});

btnDownloadRoms.addEventListener('click', async () => {
  if (!detectedUsbPath) {
    setLog('Error: Conecte un pendrive USB antes de descargar ROMs.');
    alert('Conecte un pendrive USB al Nokia 8010.');
    return;
  }

  const selectedKey = selectArcadeGame.value;
  let targetUrl = '';
  let targetFileName = '';

  if (selectedKey === 'custom') {
    targetUrl = customRomUrl.value.trim();
    if (!targetUrl) {
      alert('Introduzca la URL del archivo .zip');
      return;
    }
    targetFileName = targetUrl.substring(targetUrl.lastIndexOf('/') + 1) || 'arcade_rom.zip';
  } else {
    const item = ARCADE_DATABASE[selectedKey];
    targetUrl = item.url;
    targetFileName = item.fileName;
  }

  try {
    btnDownloadRoms.disabled = true;
    romsProgressContainer.style.display = 'block';
    romsProgressBar.style.width = '0%';
    romsProgressText.textContent = `Iniciando descarga de ${targetFileName}...`;
    setLog(`Descargando ${targetFileName} directamente al pendrive USB...`);

    const targetFolder = `${detectedUsbPath}/ROMs/arcade`;

    const res = await TvBridge.downloadZipDirectToUsb({
      fileUrl: targetUrl,
      fileName: targetFileName,
      targetFolder
    });

    lastDownloadedRomPath = res.filePath;
    setLog(`¡Éxito! Archivo guardado intacto en: ${res.filePath}`);
    romsProgressText.textContent = `¡Guardado en USB! (${targetFileName})`;
    romsProgressBar.style.width = '100%';

    if (btnLaunchRom && targetFileName !== 'neogeo.zip') {
      btnLaunchRom.style.display = 'inline-block';
      btnLaunchRom.textContent = `Lanzar ${targetFileName} en RetroArch`;
    }
  } catch (err) {
    setLog(`Error descargando ${targetFileName}: ${err.message}`);
    romsProgressText.textContent = `Error: ${err.message}`;
  } finally {
    btnDownloadRoms.disabled = false;
  }
});

btnLaunchRom.addEventListener('click', async () => {
  if (!lastDownloadedRomPath) return;
  try {
    setLog(`Iniciando ${lastDownloadedRomPath} en RetroArch...`);
    await TvBridge.launchRetroArch({
      romPath: lastDownloadedRomPath
    });
  } catch (err) {
    setLog('Error al lanzar el juego: ' + err.message);
  }
});

// Soporte de navegación para control remoto TV (flechas del teclado)
window.addEventListener('keydown', (e) => {
  if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
    // La navegación estándar por tabindex funciona nativamente en WebView
  }
});

// Inicialización y eventos de ciclo de vida
window.addEventListener('DOMContentLoaded', async () => {
  await checkPermissions();
  await checkKodi();
  await checkUsbStorage();
  await checkRetroArch();
  
  const firstFocusable = document.querySelector('button, .card');
  if (firstFocusable) firstFocusable.focus();
});

// Re-verificar cada vez que la app vuelve a primer plano (por ejemplo tras volver del instalador de APK)
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    checkRetroArch();
    checkPermissions();
    checkUsbStorage();
  }
});

window.addEventListener('focus', () => {
  checkRetroArch();
  checkPermissions();
  checkUsbStorage();
});

