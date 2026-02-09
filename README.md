# Trading Bot Framework

Dies ist ein robustes Framework für einen Trading-Bot, entwickelt, um mit virtuellem Kapital zu handeln, Gebühren zu simulieren, Verluste zu vermeiden und automatisch die beste Strategie für aktuelle Marktdaten zu finden.

## Features

- **Echte Marktdaten**: Lädt aktuelle Kryptowährungs-Daten (Standard: Bitcoin) von der Coinbase API (oder fällt auf Dummy-Daten zurück).
- **Strategie-Optimierung**: Testet automatisch verschiedene Parameter (z.B. Gleitende Durchschnitte), um die profitabelste Einstellung für die aktuellen Marktbedingungen zu finden.
- **Risikomanagement**: Verhindert, dass das Kapital unter Null fällt. Das Portfolio startet mit 100 Einheiten virtuellem Kapital.
- **Gebühren**: Simuliert realistische Handelsgebühren (Standard 0.1%).
- **Logging & Analyse**:
    - Detaillierte Logs in `logs/trading_bot.log`.
    - CSV-Export aller Testergebnisse in `optimization_results.csv`.

## Installation

1. Stelle sicher, dass Python installiert ist.
2. Installiere die Abhängigkeiten:

```bash
pip install -r requirements.txt
```

*Hinweis: `requests` wird benötigt, um Marktdaten zu laden.*

## Tests ausführen

Um sicherzustellen, dass alles korrekt funktioniert, führe die Tests aus:

```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## Bot starten (Optimierung & Simulation)

Um den Bot zu starten:

```bash
export PYTHONPATH=$PYTHONPATH:.
python main.py
```

### Was passiert dann?
1. **Daten laden**: Der Bot lädt die Bitcoin-Preise der letzten ~12 Tage.
2. **Optimierung**: Er testet verschiedene Kombinationen von "Short Window" und "Long Window" für die Strategie.
3. **Ergebnis**: Er wählt die Kombination mit dem höchsten Gewinn.
4. **Simulation**: Er führt die beste Strategie erneut aus und zeigt detaillierte Informationen zu jedem Trade an.
5. **Speichern**: Die Ergebnisse aller Tests werden in `optimization_results.csv` gespeichert.

## Ergebnisse analysieren

- **Konsole**: Zeigt den Gewinner und den ROI (Return on Investment) an.
- **optimization_results.csv**: Öffne diese Datei in Excel oder Google Sheets, um zu sehen, welche Parameter gut oder schlecht funktioniert haben. Das hilft beim "Feinschliff".
- **logs/trading_bot.log**: Hier kannst du jeden einzelnen Schritt und Trade nachvollziehen.

## Erweiterung

- **Neue Strategien**: Erstelle eine neue Klasse in `trading_bot/strategies/`, die von `Strategy` erbt.
- **Andere Coins**: Ändere in `main.py` den Parameter `coin_id` (z.B. auf 'ethereum').
- **Parameter**: Passe das `param_grid` in `main.py` an, um andere Wertebereiche zu testen.
