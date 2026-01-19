const express = require('express');
const router = express.Router();
const analysisController = require('../controllers/analysisController');
const { auth } = require('../middleware/auth');
const { uploadAnswerSheet } = require('../middleware/upload');

/**
 * @route   POST /api/analysis/upload
 * @desc    Upload answer sheet for analysis
 * @access  Private
 */
router.post('/upload', auth, uploadAnswerSheet, analysisController.uploadAndAnalyze);

/**
 * @route   GET /api/analysis/:id
 * @desc    Get analysis by ID
 * @access  Private
 */
router.get('/:id', auth, analysisController.getAnalysisById);

/**
 * @route   GET /api/analysis
 * @desc    Get all analyses for current user
 * @access  Private
 */
router.get('/', auth, analysisController.getUserAnalyses);

/**
 * @route   DELETE /api/analysis/:id
 * @desc    Delete analysis
 * @access  Private
 */
router.delete('/:id', auth, analysisController.deleteAnalysis);

/**
 * @route   GET /api/analysis/:id/download
 * @desc    Download analysis report
 * @access  Private
 */
router.get('/:id/download', auth, analysisController.downloadReport);

module.exports = router;
