/**
 * Sends email(s) using nodemailer module.
 *
 * @author Lars Petter Ulvatne, Linnaeus University.
 */
const nodeMailer = require('nodemailer')

/**
 * Sends emails to a list of emails.
 * @param emails Array of emails.
 * @param subject The subject of email to send.
 * @param html HTML code to inject into email.
 * @param message Text of HTML content.
 */
module.exports.sendMail = (emails, subject, html, message) => {
  // Can use a different SMTP server. Read documentation (npm nodemailer) for setup.
  const transporter = nodeMailer.createTransport({
    service: 'gmail',
    secure: false,
    auth: {
      user: process.env.EMAIL,
      pass: process.env.E_PASS
    }
  })

  transporter.verify(function (error, success) {
    if (error) {
      console.log(error)
    } else {
      const mailOptions = {
        from: `"Artificial grass center" <${process.env.EMAIL}>`, // sender address
        to: emails, // list of receiver(s)
        subject: subject, // Subject line
        text: message, // plain text body
        html: html
      }

      transporter.sendMail(mailOptions, (error, info) => {
        if (error) {
          console.log(error)
        }
        console.log('Successfully sent email(s).')
      })
    }
  })
}
