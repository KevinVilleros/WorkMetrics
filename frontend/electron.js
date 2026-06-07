const { app, BrowserWindow, session } = require('electron');
const path = require('path');
const isDev = process.env.NODE_ENV === 'development' || process.env.ELECTRON_START_URL;

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 840,
    icon: path.join(__dirname, 'public', 'favicon.ico'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  const startUrl = process.env.ELECTRON_START_URL || null;
  if (startUrl) {
    // Modo desarrollo - conectar a servidor React local
    win.loadURL(startUrl);
    if (isDev) {
      win.webContents.openDevTools({ mode: 'detach' });
    }
  } else {
    // Modo producción - cargar desde build
    const buildPath = path.join(__dirname, 'build', 'index.html');
    win.loadFile(buildPath);
  }

  // Manejar errores de carga
  win.webContents.on('crashed', () => {
    console.error('La aplicación se ha detenido');
  });
}

app.whenReady().then(() => {
  // Permitir acceso a cámara y micrófono
  session.defaultSession.setPermissionRequestHandler((webContents, permission, callback) => {
    if (permission === 'media') {
      callback(true);
    } else {
      callback(false);
    }
  });

  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Manejar errores no capturados
process.on('uncaughtException', (error) => {
  console.error('Error no capturado:', error);
  app.quit();
});
