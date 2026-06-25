"""
Advanced Technical Indicators Commentary Engine
===============================================
Bollinger Bands, RSI(14), and MACD crossovers translate raw numeric scores 
into rich, human-readable, and action-oriented technical commentary.
"""

from typing import Any, Dict, Optional
import numpy as np


class AdvancedTechnicalEngine:
    """
    Engine to compute and generate textual insights from technical indicators.
    Designed for professional financial interfaces to deliver actionable narratives.
    """

    @staticmethod
    def rsi_insight(rsi_value: float, ticker: str) -> Dict[str, Any]:
        """
        Generates narrative, color, and warning levels based on RSI(14) value.
        """
        symbol = ticker.upper()
        if not np.isfinite(rsi_value):
            return {
                "color": "#94A3B8",
                "emoji": "⚖️",
                "label": "VERİSİZ",
                "narrative": "RSI değeri hesaplanamadı veya veri yetersiz.",
            }

        if rsi_value >= 85:
            return {
                "color": "#EF4444",
                "emoji": "🔴🔴",
                "label": "KRİTİK AŞIRI ALIM",
                "narrative": (
                    f"RSI {rsi_value:.1f} ile tarihi aşırı alım sınırında. "
                    f"{symbol} için kar realizasyonu senaryoları masada olmalı. "
                    "Kısa vadede geri çekilme ihtimali oldukça yüksektir."
                ),
            }
        if rsi_value >= 70:
            return {
                "color": "#F97316",
                "emoji": "🔴",
                "label": "AŞIRI ALIM",
                "narrative": (
                    f"RSI {rsi_value:.1f} seviyesinde aşırı alım bölgesinde seyrediyor. "
                    "Alıcıların gücü tepe noktasına yaklaşıyor olabilir; yeni girişler için "
                    "risk katsayısı yüksektir."
                ),
            }
        if rsi_value <= 15:
            return {
                "color": "#4ADE80",
                "emoji": "🟢🟢",
                "label": "KRİTİK AŞIRI SATIM",
                "narrative": (
                    f"RSI {rsi_value:.1f} ile derin aşırı satım bölgesinde panik satışlarının "
                    f"sonuna gelindiğini işaret ediyor. {symbol} için güçlü bir tepki "
                    "yükselişi potansiyeli masada."
                ),
            }
        if rsi_value <= 30:
            return {
                "color": "#4ADE80",
                "emoji": "🟢",
                "label": "AŞIRI SATIM",
                "narrative": (
                    f"RSI {rsi_value:.1f} seviyesiyle aşırı satım bölgesinde. Hacim artış "
                    "teyidiyle beraber kademeli maliyetlenme için teknik fırsat sunabilir."
                ),
            }
        if rsi_value >= 55:
            return {
                "color": "#FBBF24",
                "emoji": "📊",
                "label": "BOĞA BÖLGESİ (GÜÇLÜ)",
                "narrative": (
                    f"RSI {rsi_value:.1f} ile pozitif bölgede konumlanıyor. Momentum "
                    "boğaların kontrolünde, yükseliş trendi koruma kalkanlarıyla destekleniyor."
                ),
            }
        if rsi_value <= 45:
            return {
                "color": "#F97316",
                "emoji": "📊",
                "label": "AYI BÖLGESİ (ZAYIF)",
                "narrative": (
                    f"RSI {rsi_value:.1f} ile nötr seviyenin altında zayıf bölgede. Satış baskısı "
                    "hakim görünüyor, dönüş sinyali teyit edilmeden alım risk taşır."
                ),
            }
        return {
            "color": "#94A3B8",
            "emoji": "⚖️",
            "label": "DENGELİ / NÖTR",
            "narrative": f"RSI {rsi_value:.1f} seviyesinde yön arayışında. Net bir trend kırılımı beklenmeli.",
        }

    @staticmethod
    def bollinger_insight(price: float, upper: float, lower: float, ticker: str) -> Dict[str, Any]:
        """
        Evaluates the current price against Bollinger Bands to produce descriptive warnings.
        """
        symbol = ticker.upper()
        if price > upper:
            return {
                "color": "#EF4444",
                "emoji": "🔴",
                "label": "BANT DIŞI - AŞIRI ALIM",
                "narrative": (
                    f"Fiyat (₺{price:.2f}), Bollinger Üst Bandını (₺{upper:.2f}) aştı. "
                    f"{symbol} bandın dışına taşarak istatistiksel sınırları zorluyor. "
                    "Genellikle bandın içerisine doğru bir düzeltme hareketi beklenir."
                ),
            }
        if price < lower:
            return {
                "color": "#4ADE80",
                "emoji": "🟢",
                "label": "BANT DIŞI - AŞIRI SATIM",
                "narrative": (
                    f"Fiyat (₺{price:.2f}), Bollinger Alt Bandının (₺{lower:.2f}) altına sarktı. "
                    f"{symbol} için panik satışlarının aşırılaştığı ve istatistiksel tepki "
                    "noktasına ulaşıldığı görülmektedir."
                ),
            }
        
        # Band içi oranlama
        band_range = upper - lower
        position = ((price - lower) / band_range) * 100 if band_range > 0 else 50.0
        return {
            "color": "#3B82F6",
            "emoji": "🔵",
            "label": "BANT İÇİ DENGELİ",
            "narrative": (
                f"Fiyat (₺{price:.2f}), Bollinger bantları içinde ve alt banda %{position:.1f} "
                "uzaklıkta dengeli seyrediyor. Majör bir aşırılık gözlemlenmiyor."
            ),
        }

    @staticmethod
    def macd_insight(macd: float, signal: float, ticker: str) -> Dict[str, Any]:
        """
        Generates insights based on MACD line and Signal line crossover.
        """
        symbol = ticker.upper()
        diff = macd - signal
        if diff > 0:
            return {
                "color": "#10B981",
                "emoji": "📈",
                "label": "BOĞA KESİŞİMİ (AL)",
                "narrative": (
                    f"MACD ({macd:.3f}), Sinyal çizgisinin ({signal:.3f}) üzerinde pozitif seyrediyor. "
                    f"Yükseliş ivmesi güç kazanmakta, {symbol} için teknik görünüm olumludur."
                ),
            }
        return {
            "color": "#EF4444",
            "emoji": "📉",
            "label": "AYI KESİŞİMİ (SAT)",
            "narrative": (
                f"MACD ({macd:.3f}), Sinyal çizgisinin ({signal:.3f}) altında negatif bölgede. "
                f"Satış baskısı devam ediyor, {symbol} için temkinli kalınmalıdır."
            ),
        }
