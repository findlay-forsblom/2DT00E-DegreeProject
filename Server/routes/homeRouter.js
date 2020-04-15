const controller = require('../controllers/homeController.js')
const express = require('express')

const router = express.Router()

router.get('/', controller.index) // Login page
router.get('/register', controller.register) // Login page

module.exports = router
