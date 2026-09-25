#!/bin/bash
set -e

echo "================================"
echo "Universal AI Platform - Test Suite"
echo "================================"
echo ""

# Setup
echo "1️⃣  Installing dependencies..."
pip install -q -r requirements.txt
pip install -q -e ".[dev]"
echo "✅ Dependencies installed"
echo ""

# Architecture Tests
echo "2️⃣  Running architecture tests..."
PYTHONPATH=src pytest -v tests/architecture/ || exit 1
echo "✅ Architecture tests passed"
echo ""

# Security Tests
echo "3️⃣  Running security tests..."
PYTHONPATH=src pytest -v tests/security/ || exit 1
echo "✅ Security tests passed"
echo ""

# Unit Tests
echo "4️⃣  Running unit tests..."
PYTHONPATH=src pytest -v tests/unit/ || exit 1
echo "✅ Unit tests passed"
echo ""

# Integration Tests
echo "5️⃣  Running integration tests..."
PYTHONPATH=src pytest -v tests/integration/ || exit 1
echo "✅ Integration tests passed"
echo ""

# Coverage Report
echo "6️⃣  Generating coverage report..."
PYTHONPATH=src pytest --cov=src --cov-report=term-missing tests/
echo ""

echo "================================"
echo "✅ All tests passed successfully!"
echo "================================"
