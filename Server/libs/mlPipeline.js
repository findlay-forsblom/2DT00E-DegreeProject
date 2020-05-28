/**
 * Spawns a python script using child_process.
 *
 * @author Findlay Forsblom, Linnaeus University.
 */

const { spawn } = require('child_process')

module.exports.getData = async (predictData) => {
  // Mac/Unix spawn by 'python3', windows spawn by 'python'.
  const python = spawn('python', ['script.py', predictData])
  let dataToSend

  const p = new Promise((resolve, reject) => {
    python.stdout.on('data', function (data) {
      dataToSend = data.toString()
      resolve()
    })
  })
  python.on('close', (code) => {
    console.log(`Prediction: Child process close all stdio with code ${code}`)
  })
  await p
  return dataToSend
}
