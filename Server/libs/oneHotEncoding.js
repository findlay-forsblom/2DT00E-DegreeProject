/**
 * One hod encodes the weather forcasts for machine learning, to match the trained data set.
 *
 * @author Findlay Forsblom, Linnaeus University.
 */

const obj = require('../app.json')
const zeros = new Array(obj.length).fill(0)

let counter = 0
const dict = {}
obj.forEach(element => {
  let i = 0
  const arr = []
  for (i = 0; i < obj.length; i++) {
    if (counter === i) {
      arr[i] = 1
    } else {
      arr[i] = 0
    }
  }
  dict[element] = arr
  counter++
})

const values = { 0: 'none', 1: 'snowfall', 2: 'snöblandat regn', 3: 'regn', 4: 'duggregn', 5: 'underkyld nederbörd' }

module.exports.encode = (precip) => {
  const arr = []
  try {
    for (const i in precip) {
      const type = values[i]
      arr.push(dict[type] || zeros)
    }
    const sums = arr[0].map(
      (x, idx) => arr.reduce((sum, curr) => sum + curr[idx], 0)
    )
    return sums
  } catch (error) {
    console.log(error)
  }
}
