package com.nokia8010.manager;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageInfo;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import android.os.storage.StorageManager;
import android.os.storage.StorageVolume;
import android.provider.Settings;
import android.util.Log;

import androidx.core.content.FileProvider;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

@CapacitorPlugin(name = "Tv8010Bridge")
public class Tv8010BridgePlugin extends Plugin {

    private static final String TAG = "Tv8010Bridge";

    // 1. Estado de permisos en Android 14
    @PluginMethod
    public void checkPermissionsStatus(PluginCall call) {
        Context context = getContext();
        JSObject ret = new JSObject();

        boolean canInstall = true;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            canInstall = context.getPackageManager().canRequestPackageInstalls();
        }

        boolean hasStorageAccess = true;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            hasStorageAccess = Environment.isExternalStorageManager();
        }

        ret.put("canInstallApk", canInstall);
        ret.put("hasStorageAccess", hasStorageAccess);
        call.resolve(ret);
    }

    @PluginMethod
    public void requestStoragePermission(PluginCall call) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
            if (!Environment.isExternalStorageManager()) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_APP_ALL_FILES_ACCESS_PERMISSION);
                intent.setData(Uri.parse("package:" + getContext().getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getContext().startActivity(intent);
            }
        }
        call.resolve();
    }

    @PluginMethod
    public void requestInstallPermission(PluginCall call) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            if (!getContext().getPackageManager().canRequestPackageInstalls()) {
                Intent intent = new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES);
                intent.setData(Uri.parse("package:" + getContext().getPackageName()));
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                getContext().startActivity(intent);
            }
        }
        call.resolve();
    }

    // 2. Detección de Kodi
    @PluginMethod
    public void checkKodiPackage(PluginCall call) {
        PackageManager pm = getContext().getPackageManager();
        JSObject ret = new JSObject();
        try {
            PackageInfo info = pm.getPackageInfo("org.xbmc.kodi", 0);
            ret.put("installed", true);
            ret.put("packageName", "org.xbmc.kodi");
            ret.put("versionName", info.versionName);
            ret.put("versionCode", info.versionCode);
        } catch (PackageManager.NameNotFoundException e) {
            ret.put("installed", false);
            ret.put("packageName", "org.xbmc.kodi");
        }
        call.resolve(ret);
    }

    // 3. Comprobar RetroArch
    @PluginMethod
    public void checkRetroArchPackage(PluginCall call) {
        PackageManager pm = getContext().getPackageManager();
        JSObject ret = new JSObject();
        String targetPkg = "com.retroarch";
        try {
            PackageInfo info = pm.getPackageInfo(targetPkg, 0);
            ret.put("installed", true);
            ret.put("packageName", targetPkg);
            ret.put("versionName", info.versionName);
        } catch (PackageManager.NameNotFoundException e) {
            try {
                PackageInfo info2 = pm.getPackageInfo("com.retroarch.aarch64", 0);
                ret.put("installed", true);
                ret.put("packageName", "com.retroarch.aarch64");
                ret.put("versionName", info2.versionName);
            } catch (PackageManager.NameNotFoundException e2) {
                ret.put("installed", false);
                ret.put("packageName", targetPkg);
            }
        }
        call.resolve(ret);
    }

    // 4. Identificar dinámicamente el pendrive USB externo
    @PluginMethod
    public void getUsbStorage(PluginCall call) {
        Context context = getContext();
        JSObject ret = new JSObject();
        ret.put("detected", false);

        try {
            // Estrategia 1: StorageManager (Android Nougat+)
            StorageManager sm = (StorageManager) context.getSystemService(Context.STORAGE_SERVICE);
            if (sm != null) {
                List<StorageVolume> volumes = sm.getStorageVolumes();
                for (StorageVolume volume : volumes) {
                    if (volume.isRemovable() && !volume.isPrimary()) {
                        String uuid = volume.getUuid();
                        File mountDir = null;
                        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
                            mountDir = volume.getDirectory();
                        }
                        
                        String path = (mountDir != null) ? mountDir.getAbsolutePath() : ("/storage/" + uuid);
                        File targetFile = new File(path);
                        if (targetFile.exists() && targetFile.canRead()) {
                            ret.put("detected", true);
                            ret.put("mountPath", path);
                            ret.put("uuid", uuid);
                            ret.put("freeSpaceBytes", targetFile.getFreeSpace());
                            ret.put("totalSpaceBytes", targetFile.getTotalSpace());
                            call.resolve(ret);
                            return;
                        }
                    }
                }
            }

            // Estrategia 2: Fallback vía getExternalFilesDirs()
            File[] externalDirs = context.getExternalFilesDirs(null);
            for (File file : externalDirs) {
                if (file != null) {
                    String fullPath = file.getAbsolutePath();
                    if (fullPath.contains("/storage/") && !fullPath.contains("/emulated/")) {
                        int idx = fullPath.indexOf("/Android/data");
                        String rootMount = (idx != -1) ? fullPath.substring(0, idx) : fullPath;
                        File rootDir = new File(rootMount);
                        ret.put("detected", true);
                        ret.put("mountPath", rootMount);
                        ret.put("freeSpaceBytes", rootDir.getFreeSpace());
                        ret.put("totalSpaceBytes", rootDir.getTotalSpace());
                        call.resolve(ret);
                        return;
                    }
                }
            }

            // Estrategia 3: Inspeccionar directamente /storage/
            File storageDir = new File("/storage");
            if (storageDir.exists() && storageDir.isDirectory()) {
                File[] list = storageDir.listFiles();
                if (list != null) {
                    for (File f : list) {
                        String name = f.getName();
                        if (!name.equalsIgnoreCase("emulated") && !name.equalsIgnoreCase("self") && f.canRead()) {
                            ret.put("detected", true);
                            ret.put("mountPath", f.getAbsolutePath());
                            ret.put("uuid", name);
                            ret.put("freeSpaceBytes", f.getFreeSpace());
                            ret.put("totalSpaceBytes", f.getTotalSpace());
                            call.resolve(ret);
                            return;
                        }
                    }
                }
            }
        } catch (Exception ex) {
            Log.e(TAG, "Error enumerando USB storage", ex);
        }

        call.resolve(ret);
    }

    // 5. Descargar RetroArch en CACHÉ e instalar
    @PluginMethod
    public void downloadAndInstallApk(PluginCall call) {
        String apkUrl = call.getString("url");
        if (apkUrl == null || apkUrl.isEmpty()) {
            call.reject("URL no proporcionada");
            return;
        }

        new Thread(() -> {
            try {
                Context context = getContext();
                File cacheDir = context.getCacheDir();
                File tempApk = new File(cacheDir, "retroarch_armv7.apk");
                if (tempApk.exists()) {
                    tempApk.delete();
                }

                URL url = new URL(apkUrl);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestProperty("User-Agent", "Mozilla/5.0 Nokia8010");
                conn.setConnectTimeout(15000);
                conn.setReadTimeout(30000);
                conn.connect();

                int responseCode = conn.getResponseCode();
                if (responseCode != HttpURLConnection.HTTP_OK) {
                    call.reject("Servidor respondió con código HTTP: " + responseCode);
                    return;
                }

                int fileLength = conn.getContentLength();
                InputStream in = new BufferedInputStream(conn.getInputStream());
                FileOutputStream out = new FileOutputStream(tempApk);

                byte[] buffer = new byte[65536];
                int count;
                long total = 0;
                long lastNotify = 0;

                while ((count = in.read(buffer)) != -1) {
                    total += count;
                    out.write(buffer, 0, count);

                    long now = System.currentTimeMillis();
                    if (now - lastNotify > 300) {
                        lastNotify = now;
                        int percent = (fileLength > 0) ? (int) ((total * 100) / fileLength) : -1;
                        JSObject progress = new JSObject();
                        progress.put("type", "retroarch");
                        progress.put("downloaded", total);
                        progress.put("total", fileLength);
                        progress.put("percent", percent);
                        notifyListeners("downloadProgress", progress);
                    }
                }

                out.flush();
                out.close();
                in.close();

                // Notificar 100%
                JSObject finalProgress = new JSObject();
                finalProgress.put("type", "retroarch");
                finalProgress.put("downloaded", total);
                finalProgress.put("total", total);
                finalProgress.put("percent", 100);
                notifyListeners("downloadProgress", finalProgress);

                // Lanzar Intent mediante FileProvider
                Uri apkUri = FileProvider.getUriForFile(
                        context,
                        context.getPackageName() + ".fileprovider",
                        tempApk
                );

                Intent installIntent = new Intent(Intent.ACTION_VIEW);
                installIntent.setDataAndType(apkUri, "application/vnd.android.package-archive");
                installIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                installIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

                context.startActivity(installIntent);

                JSObject res = new JSObject();
                res.put("success", true);
                res.put("cachedPath", tempApk.getAbsolutePath());
                call.resolve(res);

            } catch (Exception e) {
                Log.e(TAG, "Error descargando o instalando APK", e);
                call.reject("Error: " + e.getMessage(), e);
            }
        }).start();
    }

    // 6. Descarga directa de archivo .ZIP (sin descomprimir) al pendrive USB
    @PluginMethod
    public void downloadZipDirectToUsb(PluginCall call) {
        String fileUrl = call.getString("fileUrl");
        String fileName = call.getString("fileName");
        String targetFolder = call.getString("targetFolder");

        if (fileUrl == null || fileName == null || targetFolder == null) {
            call.reject("fileUrl, fileName y targetFolder son requeridos");
            return;
        }

        new Thread(() -> {
            try {
                File destDir = new File(targetFolder);
                if (!destDir.exists()) {
                    destDir.mkdirs();
                }

                File destinationFile = new File(destDir, fileName);

                URL url = new URL(fileUrl);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
                conn.setInstanceFollowRedirects(true);
                conn.setConnectTimeout(20000);
                conn.setReadTimeout(45000);
                conn.connect();

                int responseCode = conn.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_MOVED_PERM || responseCode == HttpURLConnection.HTTP_MOVED_TEMP || responseCode == 307 || responseCode == 308) {
                    String newUrl = conn.getHeaderField("Location");
                    conn.disconnect();
                    conn = (HttpURLConnection) new URL(newUrl).openConnection();
                    conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)");
                    conn.connect();
                    responseCode = conn.getResponseCode();
                }

                if (responseCode != HttpURLConnection.HTTP_OK) {
                    call.reject("Error HTTP al descargar: " + responseCode);
                    return;
                }

                int fileLength = conn.getContentLength();
                InputStream in = new BufferedInputStream(conn.getInputStream());
                FileOutputStream out = new FileOutputStream(destinationFile);

                byte[] buffer = new byte[65536];
                int count;
                long total = 0;
                long lastNotify = 0;

                while ((count = in.read(buffer)) != -1) {
                    total += count;
                    out.write(buffer, 0, count);

                    long now = System.currentTimeMillis();
                    if (now - lastNotify > 300) {
                        lastNotify = now;
                        int percent = (fileLength > 0) ? (int) ((total * 100) / fileLength) : 50;
                        JSObject progress = new JSObject();
                        progress.put("type", "roms");
                        progress.put("fileName", fileName);
                        progress.put("downloaded", total);
                        progress.put("total", fileLength);
                        progress.put("percent", percent);
                        notifyListeners("downloadProgress", progress);
                    }
                }

                out.flush();
                out.close();
                in.close();

                JSObject res = new JSObject();
                res.put("success", true);
                res.put("filePath", destinationFile.getAbsolutePath());
                res.put("sizeBytes", total);
                call.resolve(res);

            } catch (Exception e) {
                Log.e(TAG, "Error descargando archivo al USB", e);
                call.reject("Fallo al escribir en USB: " + e.getMessage(), e);
            }
        }).start();
    }

    // 7. Lanzamiento de RetroArch
    @PluginMethod
    public void launchRetroArch(PluginCall call) {
        String pkg = call.getString("packageName", "com.retroarch");
        String romPath = call.getString("romPath");

        Context context = getContext();
        PackageManager pm = context.getPackageManager();

        Intent launchIntent = pm.getLaunchIntentForPackage(pkg);
        if (launchIntent == null) {
            pkg = "com.retroarch.aarch64";
            launchIntent = pm.getLaunchIntentForPackage(pkg);
        }

        if (launchIntent == null) {
            call.reject("RetroArch no está instalado.");
            return;
        }

        try {
            Intent retroIntent = new Intent(Intent.ACTION_MAIN);
            retroIntent.setComponent(new ComponentName(pkg, "com.retroarch.browser.retroactivity.RetroActivityFuture"));
            retroIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

            if (romPath != null && !romPath.isEmpty()) {
                retroIntent.putExtra("ROM", romPath);
            }

            if (pm.resolveActivity(retroIntent, 0) != null) {
                context.startActivity(retroIntent);
            } else {
                if (romPath != null) launchIntent.putExtra("ROM", romPath);
                launchIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(launchIntent);
            }

            JSObject res = new JSObject();
            res.put("launched", true);
            call.resolve(res);
        } catch (Exception ex) {
            call.reject("Error lanzando RetroArch: " + ex.getMessage(), ex);
        }
    }
}
