"""
Unit Tests for Quantum Analytics Engine Showcase
================================================
Verifies that all math calculations, confidence multipliers, indicators thresholds, 
and correlation mappings align precisely with design specs.
"""

import numpy as np
import pandas as pd
import pytest

from core.engine import QuantumEngine
from core.indicators import AdvancedTechnicalEngine
from core.correlation import MacroCorrelationEngine


@pytest.fixture
def sample_ohlcv() -> pd.DataFrame:
    """Fixture containing mock rising prices with a volume spike."""
    dates = pd.date_range(end="2026-06-25", periods=30, freq="D")
    prices = np.linspace(80.0, 110.0, 30)
    volumes = [200000] * 29 + [400000]  # Double average volume today
    
    return pd.DataFrame({
        "open": prices * 0.99,
        "high": prices * 1.01,
        "low": prices * 0.98,
        "close": prices,
        "volume": volumes
    }, index=dates)


def test_quantum_engine_technical_score(sample_ohlcv):
    engine = QuantumEngine()
    score, meta = engine.compute_technical_score(sample_ohlcv)
    
    assert isinstance(score, float)
    assert score >= 0.0 and score <= 100.0
    assert "rsi_now" in meta
    assert "volume_ratio" in meta
    assert meta["volume_spike"] is True  # 400k vs 200k average is > 1.3x spike


def test_quantum_engine_sentiment_score():
    engine = QuantumEngine()
    
    # 1. Healthy data with 100% bullish sentiment (high post count >= 8)
    sentiment_counts_high = {"bull": 10, "bear": 0, "neutral": 0}
    score, meta = engine.compute_sentiment_score(sentiment_counts_high)
    assert score == 100.0
    assert meta["confidence_multiplier"] == 1.0
    
    # 2. Medium post count (3-7 posts) -> 0.75 multiplier
    sentiment_counts_med = {"bull": 5, "bear": 0, "neutral": 0}
    score_med, meta_med = engine.compute_sentiment_score(sentiment_counts_med)
    assert score_med == 75.0  # 100 * 0.75
    assert meta_med["confidence_multiplier"] == 0.75
    
    # 3. Low post count (< 3 posts) -> 0.50 multiplier
    sentiment_counts_low = {"bull": 2, "bear": 0, "neutral": 0}
    score_low, meta_low = engine.compute_sentiment_score(sentiment_counts_low)
    assert score_low == 50.0  # 100 * 0.50
    assert meta_low["confidence_multiplier"] == 0.50


def test_quantum_score_dynamic_weights():
    engine = QuantumEngine()
    
    # Low post count (< 5) -> Tech weight = 80%, Sentiment weight = 20%
    score_low_posts = engine.compute_quantum_score(technical_score=100.0, sentiment_score=50.0, post_count=3)
    assert score_low_posts == 90.0  # (100 * 0.8) + (50 * 0.2)
    
    # High post count (>= 5) -> Tech weight = 60%, Sentiment weight = 40%
    score_high_posts = engine.compute_quantum_score(technical_score=100.0, sentiment_score=50.0, post_count=10)
    assert score_high_posts == 80.0  # (100 * 0.6) + (50 * 0.4)


def test_advanced_technical_indicators_narratives():
    tech_engine = AdvancedTechnicalEngine()
    
    # RSI thresholds
    rsi_overbought = tech_engine.rsi_insight(88.0, "THYAO")
    assert "🔴🔴" in rsi_overbought["emoji"]
    assert "KRİTİK AŞIRI ALIM" in rsi_overbought["label"]
    
    rsi_oversold = tech_engine.rsi_insight(12.0, "THYAO")
    assert "🟢🟢" in rsi_oversold["emoji"]
    
    # Bollinger Bands
    bb_over = tech_engine.bollinger_insight(price=110.0, upper=100.0, lower=80.0, ticker="THYAO")
    assert "BANT DIŞI - AŞIRI ALIM" in bb_over["label"]
    
    bb_under = tech_engine.bollinger_insight(price=75.0, upper=100.0, lower=80.0, ticker="THYAO")
    assert "BANT DIŞI - AŞIRI SATIM" in bb_under["label"]
    
    # MACD crossover
    macd_bull = tech_engine.macd_insight(macd=0.5, signal=0.2, ticker="THYAO")
    assert "BOĞA KESİŞİMİ" in macd_bull["label"]


def test_macro_correlation_narrative():
    corr_engine = MacroCorrelationEngine()
    
    correlations = {
        "bist100": 0.85,
        "usd": -0.40,
        "gold": 0.15
    }
    
    report = corr_engine.generate_narrative("THYAO", correlations)
    
    assert "QUANTUM AI — MAKRO KORELASYON RAPORU" in report["title"]
    assert "bist100" in report["analysis"]
    assert "usd" in report["analysis"]
    assert "gold" in report["analysis"]
    
    # Check that high positive correlation with BIST is highlighted
    assert "Güçlü Pozitif" in report["analysis"]["bist100"]["narrative"]
    # Check that negative correlation with USD is highlighted
    assert "Dolar Negatif" in report["analysis"]["usd"]["narrative"]
