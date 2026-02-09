# Trading Bot Framework

Dies ist ein robustes Framework für einen Trading-Bot, entwickelt, um mit virtuellem Kapital zu handeln, Gebühren zu simulieren, Verluste zu vermeiden und automatisch die beste Strategie für aktuelle Marktdaten zu finden.

## Features

- **Echte Marktdaten**: Lädt aktuelle Kryptowährungs-Daten (Standard: Bitcoin) von der Coinbase API.
- **Strategie-Optimierung**: Testet automatisch verschiedene Parameter, um die profitabelste Einstellung für die aktuellen Marktbedingungen zu finden.
- **Live Paper Trading**: Simuliert den Handel in Echtzeit mit aktuellen Preisen.
- **Risikomanagement**: Verhindert, dass das Kapital unter Null fällt. Das Portfolio startet mit 100 Einheiten virtuellem Kapital.
- **Logging & Analyse**:
    - Detaillierte Logs in `logs/trading_bot.log`.
    - CSV-Export der Ergebnisse in `optimization_results.csv`.
    - **Live-Status**: Eine Datei `live_status.txt` wird im Live-Modus ständig aktualisiert und zeigt den aktuellen Profit/Verlust auf einen Blick.

## Installation

1. Stelle sicher, dass Python installiert ist.
2. Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Tests ausführen

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## Verwendung

### 1. Backtest & Optimierung (Standard)

Analysiert historische Daten der letzten 12 Tage und findet die beste Strategie.

```bash
export PYTHONPATH=$PYTHONPATH:.
python main.py
```

### 2. Live Paper Trading (Echtzeit)

Startet den Bot im Live-Modus.
1. Lädt historische Daten zum "Aufwärmen" der Indikatoren.
2. Optimiert die Parameter basierend auf den letzten 12 Tagen.
3. Startet eine Endlosschleife, die alle 60 Sekunden den aktuellen Bitcoin-Preis von Coinbase abruft und handelt (virtuell).

```bash
export PYTHONPATH=$PYTHONPATH:.
python main.py --live
```

Beenden mit `Ctrl+C`.

## Ergebnisse analysieren

### Im Live-Modus
Öffne die Datei `live_status.txt`. Diese wird jede Minute aktualisiert und sieht so aus:

```text
========================================
TRADING BOT LIVE STATUS
========================================
Timestamp:      2025-02-09 20:01:05
Market:         BTC/USD
Current Price:  $45123.50

STRATEGY:       LiveMAStrategy
Status:         LONG (Invested)
----------------------------------------
FINANCIALS
----------------------------------------
Cash:           $5.20
Assets (BTC/USD): 0.002100
Asset Value:    $94.76
----------------------------------------
TOTAL EQUITY:   $99.96
PROFIT/LOSS:    $-0.04 (-0.04%)
========================================
```

Das ist ideal, um auf einem zweiten Bildschirm oder in einem separaten Terminal (mit `watch cat live_status.txt`) den aktuellen Stand zu überwachen.

### Logs & CSV
- **logs/trading_bot.log**: Detaillierte Historie.
- **optimization_results.csv**: Ergebnisse der Parameter-Suche.

## Hinweise

- Der Live-Modus verwendet *kein echtes Geld*. Es ist eine Simulation mit echten Preisen ("Paper Trading").
- Die API-Rate-Limits von Coinbase sind zu beachten. Der Standard-Intervall beträgt 60 Sekunden, was sicher ist.
