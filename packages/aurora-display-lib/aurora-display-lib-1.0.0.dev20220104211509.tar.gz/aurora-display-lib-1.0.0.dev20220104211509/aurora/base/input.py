from typing import Callable, Any, Dict

from aurora.base.base import LoggingObject
from aurora.base.render import AuroraRenderTarget

AuroraInputSourceCallback = Callable[[int], Any]


class AuroraInputSource(LoggingObject):
    def __init__(self):
        super().__init__(str(self))
        self._callbacks: Dict[str, AuroraInputSourceCallback] = dict()

    def setup(self):
        self._logger.info('Setting up input source \"%s\"', self)

    def teardown(self):
        self._logger.info('Tearing down input source \"%s\"', self)
        self._logger.debug('Unregistering all %.0f callbacks ...', len(self._callbacks))
        self._callbacks.clear()

    def process(self, render_target: AuroraRenderTarget):
        pass

    def _emit_callback(self, key: int):
        for callback_id in self._callbacks:
            self._logger.debug('Invoking callback %s ...', callback_id)
            try:
                self._callbacks[callback_id](key)
            except Exception as e:
                self._logger.error('Error while emitting callback %s for keyboard event: %s', callback_id, e)

    def register_callback(self,
                          callback_id: str,
                          callback: AuroraInputSourceCallback):
        if not callback_id:
            raise AssertionError('Callback ID must be provided!')
        self._logger.info('Registered new callback with ID %s', callback_id)
        self._callbacks[callback_id] = callback

    def unregister_callback(self,
                            callback_id: str):
        if not callback_id:
            raise AssertionError('Callback ID must be provided!')
        self._logger.info('Unregistering callback with ID %s', callback_id)
        self._callbacks.pop(callback_id)

    def __str__(self) -> str:
        return 'V2InputSource (not implemented)'

    def __repr__(self) -> str:
        return 'V2InputSource (not implemented)'


class NullInputSource(AuroraInputSource):
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return 'NULL input source'

    def __repr__(self) -> str:
        return 'NULL input source'
