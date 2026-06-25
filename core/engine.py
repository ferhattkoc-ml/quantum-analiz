"""
Quantum Integration & Cross-Signal Engine
==========================================
Clashes classical technical analysis (RSI dip recovery, volume spikes) 
with social/community sentiment to generate a unified, weighted "Quantum Score" (0-100).
"""

from typing import Any, Dict, Tuple
import pandas as pd
import numpy as np


class QuantumEngine:
    """
    Core consolidation engine for multi-dimensional quantitative and sentiment signal cross-evaluation.
    """

    def __init__(self, technical_weight_default: float = 0.60):
        self.tech_weight_default = technical_weight_default
        self.senti_weight_default = 1.0 - technical_weight_default

    def compute_technical_score(self, df: pd.DataFrame) -> Tuple[float, Dict[str, Any]]:
        """
        Generates a Technical Score (0-100) based on OHLCV data.
        
        Components:
          - RSI Dip Recovery (RSI dropped below 35 in the last 5 days and recovered above 45) → Max 60 points.
          - Volume Spike (today's volume vs 20-day average volume > 1.30) → Max 40 points.
        """
        meta = {
            "rsi_now": None,
            "volume_ratio": None,
            "rsi_dip_recovery": False,
            "volume_spike": False,
        }

        if df is None or df.empty or "close" not in df.columns or len(df) < 25:
            return 0.0, meta

        close_series = df["close"].astype(float)
        
        # Simple RSI implementation
        delta = close_series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        rsi_now = float(rsi.iloc[-1]) if rsi.dropna().size else 50.0
        rsi_min5 = float(rsi.tail(6).min()) if rsi.tail(6).dropna().size else 50.0

        rsi_score = 0.0
        if rsi_min5 < 35.0 and rsi_now > 45.0:
            # Full dip recovery
            base_score = 60.0
            # If RSI went too high (e.g. overbought > 65), slightly decay its score
            if rsi_now > 65.0:
                base_score = max(30.0, 60.0 - (rsi_now - 65.0) * 1.5)
            rsi_score = base_score
            meta["rsi_dip_recovery"] = True
        elif rsi_min5 < 40.0 and rsi_now > 42.0:
            # Soft dip recovery
            rsi_score = 30.0

        volume_score = 0.0
        vol_ratio = 1.0
        if "volume" in df.columns and len(df) >= 21:
            vol_today = float(df["volume"].iloc[-1] or 0)
            vol_avg20 = float(df["volume"].iloc[-21:-1].mean() or 1)
            if vol_avg20 > 0:
                vol_ratio = vol_today / vol_avg20
                if vol_ratio >= 1.30:
                    # 1.30 ratio -> 20 points, 2.0+ ratio -> 40 points (capped)
                    volume_score = min(40.0, 20.0 + (vol_ratio - 1.30) * 28.6)
                    meta["volume_spike"] = True

        meta["rsi_now"] = round(rsi_now, 2)
        meta["volume_ratio"] = round(vol_ratio, 2)
        
        total_technical = round(rsi_score + volume_score, 2)
        return total_technical, meta

    def compute_sentiment_score(self, sentiment_counts: Dict[str, int]) -> Tuple[float, Dict[str, Any]]:
        """
        Computes Sentiment Score (0-100) based on social post sentiment distribution.
        
        Confidence Multipliers:
          - High activity (>= 8 posts) → 1.0x confidence
          - Medium activity (3-7 posts) → 0.75x confidence
          - Low activity (< 3 posts) → 0.5x confidence (discounted due to low sample size)
        """
        meta = {
            "bull_ratio": 0.0,
            "bear_ratio": 0.0,
            "neutral_ratio": 0.0,
            "post_count": 0,
            "confidence_multiplier": 1.0,
        }

        bull = sentiment_counts.get("bull", 0)
        bear = sentiment_counts.get("bear", 0)
        neutral = sentiment_counts.get("neutral", 0)
        total = bull + bear + neutral
        
        meta["post_count"] = total
        if total == 0:
            return 0.0, meta

        bull_ratio = bull / total
        bear_ratio = bear / total
        neutral_ratio = neutral / total

        meta["bull_ratio"] = round(bull_ratio, 3)
        meta["bear_ratio"] = round(bear_ratio, 3)
        meta["neutral_ratio"] = round(neutral_ratio, 3)

        # Net sentiment stance mapping: (Bull - Bear) from [-1..1] to [0..100]
        net_stance = bull_ratio - bear_ratio
        raw_sentiment = (net_stance + 1.0) * 50.0

        # Apply confidence multipliers based on count
        if total < 3:
            multiplier = 0.50
        elif total < 8:
            multiplier = 0.75
        else:
            multiplier = 1.00

        meta["confidence_multiplier"] = multiplier
        final_sentiment = round(raw_sentiment * multiplier, 2)

        return final_sentiment, meta

    def compute_quantum_score(
        self, technical_score: float, sentiment_score: float, post_count: int
    ) -> float:
        """
        Combines technical and sentiment scores dynamically based on community popularity.
        
        - If social post count is low (< 5), technical indicators dominate (80% weight).
        - If social post count is healthy (>= 5), weights normalize (60% tech / 40% sentiment).
        """
        if post_count < 5:
            weight_tech = 0.80
        else:
            weight_tech = self.tech_weight_default

        weight_senti = 1.0 - weight_tech
        quantum_score = (weight_tech * technical_score) + (weight_senti * sentiment_score)
        return round(quantum_score, 2)

    def determine_signal_reason(self, technical_score: float, sentiment_score: float) -> str:
        """
        Categorizes the primary driver of the quantum buy signal.
        """
        if technical_score >= 60.0 and sentiment_score >= 60.0:
            return "BOTH (TEKNİK & SOSYAL GÜÇ)"
        if technical_score >= 60.0:
            return "TECHNICAL (TEKNİK DÖNÜŞ)"
        if sentiment_score >= 60.0:
            return "SOCIAL (SOSYAL COŞKU)"
        return "WEAK (ZAYIF SİNYAL)"

    def build_quantum_report(
        self, ticker: str, df: pd.DataFrame, sentiment_counts: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Orchestrates and builds a full Quantum Analysis Report for a given asset.
        """
        tech_score, tech_meta = self.compute_technical_score(df)
        senti_score, senti_meta = self.compute_sentiment_score(sentiment_counts)
        quantum_score = self.compute_quantum_score(tech_score, senti_score, senti_meta["post_count"])
        signal_reason = self.determine_signal_reason(tech_score, senti_score)

        return {
            "ticker": ticker.upper(),
            "quantum_score": quantum_score,
            "signal_reason": signal_reason,
            "technical_score": tech_score,
            "technical_meta": tech_meta,
            "sentiment_score": senti_score,
            "sentiment_meta": senti_meta,
            "status": "STRONG BUY" if quantum_score >= 70 else "BUY" if quantum_score >= 55 else "HOLD",
        }
