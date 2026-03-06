// Simplified ClawFeed Server - No SQLite dependency
const express = require('express');
const app = express();
const port = 8767;

// In-memory storage for demo
let digests = [];
let sources = [];

// Simple routes
app.get('/api/digests', (req, res) => {
  res.json({ results: digests, number_of_results: digests.length });
});

app.get('/api/sources', (req, res) => {
  res.json(sources);
});

app.post('/api/sources', express.json(), (req, res) => {
  const source = req.body;
  sources.push(source);
  res.json({ success: true, id: sources.length });
});

app.get('/', (req, res) => {
  res.send('<h1>Simplified ClawFeed</h1><p>API running on port 8767</p>');
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Simplified ClawFeed server running at http://localhost:${port}`);
});