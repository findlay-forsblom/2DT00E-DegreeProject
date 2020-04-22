const controller = require('../controllers/actionController.js')
const express = require('express')

const router = express.Router()

router.get('/clear/:id/:date', controller.clear)
router.get('/close/:id/:date', controller.close)
router.get('/:id', controller.index)

module.exports = router
