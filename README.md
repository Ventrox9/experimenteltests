# Trading Bot Framework

Dies ist ein robustes Framework für einen Trading-Bot, entwickelt, um mit virtuellem Kapital zu handeln, Gebühren zu simulieren, Verluste zu vermeiden und automatisch die beste Strategie für aktuelle Marktdaten zu finden.

## Features

- **Echte Marktdaten**: Lädt aktuelle Kryptowährungs-Daten (Standard: Bitcoin) von der Coinbase API.
- **Strategie-Optimierung**: Testet automatisch verschiedene Parameter, um die profitabelste Einstellung für die aktuellen Marktbedingungen zu finden.
- **Live Paper Trading**: Simuliert den Handel in Echtzeit mit aktuellen Preisen.
- **Risikomanagement**: Verhindert, dass das Kapital unter Null fällt. Das Portfolio startet mit 100 Einheiten virtuellem Kapital.
- **Logging & Analyse**: Detaillierte Logs in `logs/trading_bot.log` und CSV-Export.

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

- **Konsole**: Zeigt Live-Status ("Current Price", "Waiting for next tick...") und Trades.
- **logs/trading_bot.log**: Detaillierte Aufzeichnungen aller Aktionen.
- **optimization_results.csv**: Ergebnisse der Parameter-Suche.

## Hinweise

- Der Live-Modus verwendet *kein echtes Geld*. Es ist eine Simulation mit echten Preisen ("Paper Trading").
- Die API-Rate-Limits von Coinbase sind zu beachten. Der Standard-Intervall beträgt 60 Sekunden, was sicher ist.
