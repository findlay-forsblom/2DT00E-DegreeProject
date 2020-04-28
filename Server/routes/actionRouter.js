const controller = require('../controllers/actionController.js')
const express = require('express')

const router = express.Router()

router.get('/:id', controller.ensureAuthenticated, controller.authorize, controller.index)
router.get('/', controller.ensureAuthenticated, controller.index)

router.post('/decision/', controller.ensureAuthenticated, controller.authorize, controller.decision)

module.exports = router
