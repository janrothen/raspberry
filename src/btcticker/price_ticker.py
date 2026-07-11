import logging
import time

from btcticker.display import Display
from btcticker.frame_renderer import FrameRenderer
from btcticker.price.protocols import PriceFormatter, PriceSource

DEFAULT_REFRESH_INTERVAL = 300  # seconds
FAILED_REFRESH_RETRY_SECONDS = 60  # re-poll sooner while showing "N/A"
INTRO_PAUSE_SECONDS = 3
IDLE_SLEEP_SECONDS = 1


class PriceTicker:
    """Orchestrates price refresh cycles on the e-paper display.

    Owns the refresh schedule and the display lifecycle. Delegates
    frame composition to the renderer and price data to the client/extractor.
    """

    def __init__(
        self,
        display: Display,
        renderer: FrameRenderer,
        price_client: PriceSource,
        price_extractor: PriceFormatter,
        refresh_interval: int = DEFAULT_REFRESH_INTERVAL,
    ) -> None:
        self.display = display
        self.renderer = renderer
        self.price_client = price_client
        self.price_extractor = price_extractor
        self._refresh_interval = refresh_interval
        self._next_interval = refresh_interval
        self._started = False
        self._stopped = False
        self._last_refresh = float("-inf")  # guarantees refresh on first tick()

    def start(self) -> None:
        """Display the intro image and pause before the price loop begins.

        No-op on repeated calls.
        """
        if self._started:
            return
        self._started = True
        self.display.show(self.renderer.render_intro())
        time.sleep(INTRO_PAUSE_SECONDS)

    def tick(self) -> None:
        """Run one iteration of the price refresh loop. Call repeatedly from main."""
        if time.monotonic() - self._last_refresh < self._next_interval:
            time.sleep(IDLE_SLEEP_SECONDS)
            return

        data = self.price_client.retrieve_data()
        price = self.price_extractor.formatted_price_from_data(data)
        frame = self.renderer.render_price(price)

        self.display.init()
        self.display.show(frame)
        self.display.sleep()
        self._last_refresh = time.monotonic()
        # After a failed fetch, retry sooner so "N/A" doesn't linger for the
        # full refresh interval once connectivity returns.
        self._next_interval = (
            self._refresh_interval
            if data is not None
            else min(self._refresh_interval, FAILED_REFRESH_RETRY_SECONDS)
        )

    def stop(self) -> None:
        if self._stopped:
            return
        self._stopped = True
        logging.info("shutting down")
        try:
            self.display.init()
            self.display.clear()
            self.display.sleep()
        except Exception:
            logging.exception("display shutdown failed")
