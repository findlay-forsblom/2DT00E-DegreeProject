const controller = require('../controllers/homeController.js')
const express = require('express')

const router = express.Router()

router.get('/', controller.index) // Login page
router.get('/:id', controller.index)
router.post('/login', controller.login)
router.post('/logout', controller.logout)

router.route('/register')
  .get(controller.register)
  .post(controller.registerPost)

module.exports = router
