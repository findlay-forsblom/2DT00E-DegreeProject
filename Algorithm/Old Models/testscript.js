const fs = require('fs');
const path = require('path');

  // Buffer mydata
const BUFFER = bufferFile('./Models/multipleLinearReg');

console.log(BUFFER)

  function bufferFile(relPath) {
    return fs.readFileSync(path.join(__dirname, relPath)); // zzzz....
  }