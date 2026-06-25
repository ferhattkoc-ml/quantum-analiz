"""
Quantum Analytics Engine - Showcase Application
==============================================
Simulates the core analytical engines using generated mock data for a showcase run.
Shows BIST traders how indicators, sentiment, and macro correlation are integrated.
"""

import numpy as np
import pandas as pd
from core.engine import QuantumEngine
from core.indicators import AdvancedTechnicalEngine
from core.correlation import MacroCorrelationEngine


def generate_mock_ohlcv(days: int = 30, trend: str = "bullish") -> pd.DataFrame:
    """
    Generates a realistic mock pandas DataFrame for OHLCV prices.
    """
    np.random.seed(42)
    dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq="D")
    
    # Simulating price
    if trend == "bullish":
        price_changes = np.random.normal(loc=0.005, scale=0.02, size=days)
    else:
        price_changes = np.random.normal(loc=-0.005, scale=0.02, size=days)
        
    prices = 100.0 * np.exp(np.cumsum(price_changes))
    
    # Adding volume spikes on the last few days
    volumes = np.random.randint(100000, 500000, size=days)
    volumes[-1] = int(volumes[:-1].mean() * 1.85)  # Significant volume spike today (1.85x)

    df = pd.DataFrame({
        "open": prices * 0.99,
        "high": prices * 1.01,
        "low": prices * 0.98,
        "close": prices,
        "volume": volumes
    }, index=dates)
    
    return df


def generate_mock_macro_returns(days: int = 120) -> pd.DataFrame:
    """
    Generates return series for BIST100, USD, and Gold.
    """
    np.random.seed(100)
    bist100_rets = np.random.normal(0.001, 0.015, size=days)
    usd_rets = np.random.normal(0.0005, 0.004, size=days)
    gold_rets = np.random.normal(0.0002, 0.012, size=days)
    
    return pd.DataFrame({
        "bist100": bist100_rets,
        "usd": usd_rets,
        "gold": gold_rets
    })


def run_showcase():
    print("=" * 80)
    print("🌌 QUANTUM ANALYTICS ENGINE — PUBLIC PORTFOLIO SHOWCASE")
    print("=" * 80)
    print("Sanal BIST Veri Seti Üzerinde Analiz Motoru Çalıştırılıyor...\n")

    ticker = "THYAO"
    
    # 1. GENERATE DATA
    print("📥 [1/4] Yapay Piyasa ve Topluluk Verileri Hazırlanıyor...")
    # Generate OHLCV with a dip recovery and volume spike
    ohlcv_df = generate_mock_ohlcv(days=35, trend="bullish")
    # Tweak last days close/rsi for dip recovery simulation
    # Let's override values to simulate deep RSI recovery
    ohlcv_df.iloc[-10:-4, ohlcv_df.columns.get_loc("close")] = 85.0   # Drop price to create low RSI
    ohlcv_df.iloc[-4:, ohlcv_df.columns.get_loc("close")] = 110.0     # Rapid recovery
    
    # Sentiment Counts from social posts
    sentiment_counts = {
        "bull": 14,
        "bear": 2,
        "neutral": 4
    }
    
    print(f"Hisse: {ticker}")
    print(f"Son Fiyat: ₺{ohlcv_df['close'].iloc[-1]:.2f}")
    print(f"Son Hacim: {ohlcv_df['volume'].iloc[-1]:,} adet")
    print(f"Sosyal Topluluk Paylaşımları: {sentiment_counts['bull']} Boğa, {sentiment_counts['bear']} Ayı, {sentiment_counts['neutral']} Nötr")
    print("-" * 80)

    # 2. QUANTUM CROSS SIGNAL ENGINE
    print("\n⚡ [2/4] Quantum Signal Cross Motoru Çalıştırılıyor...")
    engine = QuantumEngine()
    report = engine.build_quantum_report(ticker, ohlcv_df, sentiment_counts)
    
    print(f">>> QUANTUM SKORU      : {report['quantum_score']} / 100")
    print(f">>> DETAYLI TEKNİK SKOR: {report['technical_score']} / 100")
    print(f">>> DETAYLI SOSYAL SKOR: {report['sentiment_score']} / 100")
    print(f">>> DEĞERLENDİRME      : {report['status']}")
    print(f">>> SİNYAL TETİKLEYİCİ : {report['signal_reason']}")
    print(f"    [Teknik Detay] RSI: {report['technical_meta']['rsi_now']} | Dipten Dönüş: {report['technical_meta']['rsi_dip_recovery']} | Hacim Patlaması: {report['technical_meta']['volume_spike']}")
    print(f"    [Sosyal Detay] Boğa Oranı: %{report['sentiment_meta']['bull_ratio']*100:.1f} | Toplam Post: {report['sentiment_meta']['post_count']}")
    print("-" * 80)

    # 3. ADVANCED TECHNICAL INDICATORS COMMENTARY
    print("\n📊 [3/4] İleri Teknik Göstergeler Doğal Yorumlama Motoru:")
    tech_engine = AdvancedTechnicalEngine()
    
    rsi_val = float(report['technical_meta']['rsi_now'])
    rsi_out = tech_engine.rsi_insight(rsi_val, ticker)
    bb_out = tech_engine.bollinger_insight(
        price=ohlcv_df['close'].iloc[-1],
        upper=ohlcv_df['close'].iloc[-1] * 1.05,
        lower=ohlcv_df['close'].iloc[-1] * 0.92,
        ticker=ticker
    )
    macd_out = tech_engine.macd_insight(macd=0.450, signal=0.120, ticker=ticker)
    
    print(f"\n {rsi_out['emoji']} {rsi_out['label']} (RSI)")
    print(f"   {rsi_out['narrative']}")
    
    print(f"\n {bb_out['emoji']} {bb_out['label']} (Bollinger)")
    print(f"   {bb_out['narrative']}")
    
    print(f"\n {macd_out['emoji']} {macd_out['label']} (MACD)")
    print(f"   {macd_out['narrative']}")
    print("-" * 80)

    # 4. MACRO CORRELATION ENGINE
    print("\n📈 [4/4] Makro Korelasyon Analiz Motoru:")
    corr_engine = MacroCorrelationEngine()
    
    # Generate mock return series for asset and macro assets
    macro_df = generate_mock_macro_returns(days=120)
    asset_returns = pd.Series(np.random.normal(0.0012, 0.016, size=120))
    # Tweak correlations to simulate highly positive BIST but gold hedging
    # Make asset return highly correlated to BIST100
    asset_returns = macro_df["bist100"] * 0.85 + np.random.normal(0, 0.005, size=120)
    
    corr_results = corr_engine.calculate_correlations(asset_returns, macro_df)
    # Ensure slightly negative gold/usd correlation for hedge showcase
    corr_results["gold"] = -0.245
    corr_results["usd"] = 0.120
    
    corr_report = corr_engine.generate_narrative(ticker, corr_results)
    
    print(f"Sanal Korelasyon Katsayıları (Pearson - 6 Ay):")
    print(f"  - BIST100: {corr_results['bist100']:+.3f}")
    print(f"  - USD/TRY: {corr_results['usd']:+.3f}")
    print(f"  - ONS ALTIN: {corr_results['gold']:+.3f}")
    
    print(f"\n📋 {corr_report['title']}")
    print(f"   Kılavuz: {corr_report['legend']}")
    
    print("\n   Varlık Analizleri:")
    for asset_name, details in corr_report['analysis'].items():
        print(f"   ▫️ {asset_name.upper()} İlişkisi:")
        print(f"      {details['narrative']}")
        print(f"      {details['tip']}")
        
    print("\n" + "=" * 80)
    print("🌌 SİMÜLASYON BAŞARIYLA TAMAMLANDI")
    print("=" * 80)


if __name__ == "__main__":
    run_showcase()
