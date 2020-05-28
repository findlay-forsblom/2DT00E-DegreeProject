
/**
 * Creates and returns object of three consecutive days, from the input parameter day.
 * @param {Date} today Date object
 *
 * @author Lars Petter Ulvatne
 */

function consecutiveDays (today = new Date()) {
  const oneDay = new Date()
  oneDay.setDate(today.getDate() + 1)
  const twoDays = new Date()
  twoDays.setDate(today.getDate() + 2)

  return { today: today, oneDay: oneDay, twoDays: twoDays }
}

module.exports = { consecutiveDays }
