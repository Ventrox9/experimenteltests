from trading_bot.strategies.simple_ma import SimpleMAStrategy

class LiveMAStrategy(SimpleMAStrategy):
    """
    Subclass for Live Trading.
    Ideally, we would modify SimpleMAStrategy to handle warmup gracefully,
    but for now, we can just reset state after warmup.
    """
    def reset(self):
        """Reset trading position but keep indicators (deque)."""
        self.position = 0
        self.log("Strategy Reset (Indicators Preserved)")
