const { spawn } = require('child_process')

module.exports.getData = async (testData) => {
  const python = spawn('python', ['script.py', testData])
  let dataToSend

  const p = new Promise((resolve, reject) => {
    python.stdout.on('data', function (data) {
      dataToSend = data.toString()
      console.log(dataToSend)
      resolve()
    })
  })
  python.on('close', (code) => {
    console.log(`child process close all stdio with code ${code}`)
  })
  await p
  return dataToSend
}
