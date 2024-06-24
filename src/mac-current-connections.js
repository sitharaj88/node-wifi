const promiser = require('./utils/promiser');
const { exec } = require('child_process');
const path = require('path');

const currentConnectionWifi =  (config) => {
  console.log('Scanning current wifi connection...')
  console.log(config);
  return new Promise((resolve, reject) => {
    const pythonScriptPath = path.join(__dirname, './macOS/current-connections/list_current_wifi_connections.py');
    exec(`python3 ${pythonScriptPath}`, (error, stdout, stderr) => {
      if (error) {
        reject(`Error: ${error.message}`);
      } else if (stderr) {
        reject(`Stderr: ${stderr}`);
      } else {
        try {
          const result = JSON.parse(stdout);
          if (result.success) {
            resolve(result);
          } else {
            reject(result.error);
          }
        } catch (e) {
          reject(`Parsing error: ${e.message}`);
        }
      }
    });
  });
};

module.exports = promiser(currentConnectionWifi);
