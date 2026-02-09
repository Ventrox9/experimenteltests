# Trading Bot Framework

Dies ist ein robustes Framework für einen Trading-Bot, entwickelt, um mit virtuellem Kapital zu handeln, Gebühren zu simulieren und Verluste zu vermeiden.

## Features

- **Modulare Struktur**: Trennung von Exchange, Portfolio, Strategie und Ausführungs-Engine.
- **Risikomanagement**: Verhindert, dass das Kapital unter Null fällt. Das Portfolio startet mit 100 Einheiten virtuellem Kapital.
- **Gebühren**: Simuliert realistische Handelsgebühren (Standard 0.1%).
- **Parallele Strategien**: Unterstützt das gleichzeitige Ausführen mehrerer Strategien zum Vergleich.
- **Logging**: Detaillierte Aufzeichnungen aller Trades und Fehler in `logs/trading_bot.log`.

## Installation

Stelle sicher, dass Python installiert ist. Es werden keine externen Bibliotheken für den Kern benötigt, aber `pytest` wird für die Tests empfohlen.

```bash
pip install pytest
```

## Tests ausführen

Um sicherzustellen, dass alles korrekt funktioniert, führe die Tests aus:

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## Simulation starten

Um den Bot mit simulierten Marktdaten laufen zu lassen:

```bash
export PYTHONPATH=$PYTHONPATH:.
python main.py
```

Der Bot generiert zufällige Marktdaten und lässt zwei Beispiel-Strategien darauf laufen:
1. `MA_Strategy_Standard` (Langsamerer gleitender Durchschnitt)
2. `MA_Strategy_Fast` (Schnellerer gleitender Durchschnitt)

## Ergebnisse & Logs

Nach dem Durchlauf findest du eine Zusammenfassung in der Konsole und detaillierte Logs in `logs/trading_bot.log`.

Beispielhafte Ergebnisse aus einem Testlauf:
- **MA_Strategy_Standard**: Wenig Aktivität, Kapitalerhalt.
- **MA_Strategy_Fast**: Aggressiverer Handel, potenziell höherer Gewinn (aber auch höheres Risiko).

Die genauen Ergebnisse hängen von den generierten Zufallsdaten ab.

## Erweiterung

Neue Strategien können einfach durch Erben von `Strategy` in `trading_bot/strategy.py` erstellt und in `main.py` eingebunden werden.
