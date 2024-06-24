const promiser = require('./utils/promiser');
const { exec } = require('child_process');
const path = require('path');


const scanWifi =  (config) => {
  console.log('Scanning wifi networks...')
  console.log(config);
  return new Promise((resolve, reject) => {
    const pythonScriptPath = path.join(__dirname, './macOS/scan/scan_ssids.py');
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
  

module.exports = promiser(scanWifi);
