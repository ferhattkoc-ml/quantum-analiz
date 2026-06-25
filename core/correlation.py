"""
Macro Correlation Analytics Engine
===================================
Analyzes statistical correlations of asset returns against major macro assets 
(BIST100 index, Dolar/TRY, Ons Gold) to determine beta alignment or portfolio hedging potential.
"""

from typing import Any, Dict, List
import pandas as pd
import numpy as np


class MacroCorrelationEngine:
    """
    Engine to calculate and interpret correlation matrices for financial assets.
    Helps developers and investors build hedging strategies based on daily return series.
    """

    @staticmethod
    def calculate_correlations(asset_returns: pd.Series, macro_returns_df: pd.DataFrame) -> Dict[str, float]:
        """
        Computes Pearson correlation coefficients of an asset's returns against a DataFrame of macro asset returns.
        
        :param asset_returns: Daily log or simple percentage returns of the target asset.
        :param macro_returns_df: DataFrame containing columns: 'bist100', 'usd', 'gold' with aligned returns.
        :return: Dict containing correlation coefficient values.
        """
        results = {"bist100": 0.0, "usd": 0.0, "gold": 0.0}
        if asset_returns is None or asset_returns.empty or macro_returns_df is None or macro_returns_df.empty:
            return results

        # Align series by index (date alignment)
        aligned_df = macro_returns_df.copy()
        aligned_df["asset"] = asset_returns

        # Compute Pearson correlation matrix
        corr_matrix = aligned_df.corr(method="pearson")
        
        for key in results.keys():
            if key in corr_matrix.columns and "asset" in corr_matrix.index:
                val = corr_matrix.loc["asset", key]
                results[key] = round(float(val), 3) if np.isfinite(val) else 0.0

        return results

    @staticmethod
    def generate_narrative(ticker: str, correlations: Dict[str, float]) -> Dict[str, Any]:
        """
        Translates raw correlation coefficients into highly detailed Turkish financial insights.
        """
        symbol = ticker.upper()
        cb = correlations.get("bist100", 0.0)
        cu = correlations.get("usd", 0.0)
        cg = correlations.get("gold", 0.0)

        heatmap_legend = (
            "1'e yakın değerler (lacivert) → aynı yönlü hareket | "
            "-1'e yakın değerler (kırmızı) → ters yönlü hareketi ifade eder. "
            "Negatif korelasyonlu varlıklar portföy sigortası (hedge) görevi görür."
        )

        # ── BIST100 Yorumu ──
        if cb >= 0.75:
            bist_para = (
                f"Güçlü Pozitif ({cb:+.2f}) — {symbol}, BIST100 endeksi ile son derece yüksek uyum içinde. "
                "Hisse senedi, endeks yükseliş dalgalarını çarpan etkisiyle yakalamaya yatkındır."
            )
            bist_tip = "📌 Endeks boğa piyasasındayken pozisyon korumak veya büyütmek avantajlı olabilir."
        elif cb >= 0.40:
            bist_para = (
                f"Orta Pozitif ({cb:+.2f}) — {symbol} endeks yönüyle kısmen uyumlu ancak kendi içsel dinamiklerini koruyor. "
                "Ayrışma (alfa) potansiyeli mevcuttur."
            )
            bist_tip = "📌 Endeks analizine ek olarak, hisseye özel finansal rasyoları ve haber akışlarını takip edin."
        elif cb >= 0.0:
            bist_para = (
                f"Zayıf Pozitif ({cb:+.2f}) — {symbol} ile endeks arasında belirgin bir istatistiksel bağ bulunmuyor. "
                "Hisse, şirkete özel gelişmeler ve temel verilerle şekillenmektedir."
            )
            bist_tip = "📌 Sektörel katalizörlere, bilanço performansına ve büyüme rasyolarına odaklanın."
        else:
            bist_para = (
                f"Negatif ({cb:+.2f}) — {symbol}, BIST100 ile ters yönlü hareket etme eğiliminde. "
                "Piyasa düşüşlerinde güçlü bir defansif duruş sergileyebilir."
            )
            bist_tip = "📌 Portföyün genel BIST100 beta riskini düşürmek ve hedge etmek için koruyucu rol üstlenir."

        # ── USD/TRY Yorumu ──
        if cu >= 0.60:
            usd_para = (
                f"Güçlü Dolar Pozitif ({cu:+.2f}) — Dolar kuru yükseldikçe {symbol} de değer kazanmaktadır. "
                "Şirketin döviz pozisyonu fazlası, ihracat payının yüksekliği veya dövize endeksli gelir modeli bu etkiyi destekler."
            )
            usd_tip = "📌 Kur yükseliş senaryolarında portföyde döviz koruması olarak değerlendirilebilir."
        elif cu <= -0.30:
            usd_para = (
                f"Dolar Negatif ({cu:+.2f}) — Kur artışı {symbol} üzerinde maliyet baskısı yaratmakta veya "
                "döviz borçluluğu nedeniyle bilançoyu olumsuz etkilemektedir."
            )
            usd_tip = "📌 Kur oynaklığının yüksek olduğu dönemlerde taşınan riskler minimize edilmelidir."
        else:
            usd_para = (
                f"Nötr Dolar İlişkisi ({cu:+.2f}) — {symbol} hissesinin döviz kuru dalgalanmalarıyla doğrudan "
                "bir korelasyonu saptanmamıştır."
            )
            usd_tip = "📌 Kur hareketlerinden ziyade operasyonel karlılık rasyolarını izleyin."

        # ── Ons Altın Yorumu ──
        if cg >= 0.40:
            gold_para = (
                f"Altın Pozitif ({cg:+.2f}) — Altın fiyatlarındaki yükseliş {symbol} hissesini "
                "pozitif etkilemektedir. Değerli maden madenciliği veya yüksek nakit/altın rezervi etken olabilir."
            )
            gold_tip = "📌 Küresel risklerden kaçış dönemlerinde altındaki yükselişle beraber hisse de izlenmelidir."
        elif cg <= -0.30:
            gold_para = (
                f"Altın Negatif ({cg:+.2f}) — Altın fiyatlarının yükselmesi (güvenli liman arayışı), "
                f"riskli varlıklar arasında bulunan {symbol} üzerinde baskı yaratmaktadır."
            )
            gold_tip = "📌 Küresel emtia rallilerinde hissenin göreceli zayıf kalabileceği göz önünde bulundurulmalıdır."
        else:
            gold_para = (
                f"Altın Nötr ({cg:+.2f}) — Altın fiyat hareketleri ile {symbol} arasında "
                "doğrudan anlamlı bir istatistiksel ilişki bulunmamaktadır."
            )
            gold_tip = "📌 Emtia trendlerinden ziyade ulusal piyasa dinamiklerine odaklanın."

        return {
            "title": "QUANTUM AI — MAKRO KORELASYON RAPORU",
            "legend": heatmap_legend,
            "correlations": {
                "bist100": cb,
                "usd": cu,
                "gold": cg,
            },
            "analysis": {
                "bist100": {"narrative": bist_para, "tip": bist_tip},
                "usd": {"narrative": usd_para, "tip": usd_tip},
                "gold": {"narrative": gold_para, "tip": gold_tip},
            },
        }
