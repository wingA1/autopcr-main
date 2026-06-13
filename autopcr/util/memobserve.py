import asyncio

from ..constants import MEMORY_OBSERVE_INTERVAL
from ..core.clientpool import instance as clientpool
from ..http_server.validator import validate_dict, validate_ok_dict, cleanup_validate_cache
from ..module.crons import background_task_count
from ..util.logger import instance as logger

_observer_task = None


async def _memory_observer():
    while True:
        await asyncio.sleep(MEMORY_OBSERVE_INTERVAL)
        cleanup_validate_cache()
        logger.info(
            "memory observe: validate_qids=%d validate_pending=%d "
            "validate_ok=%d client_pool_idle=%d client_pool_active=%d "
            "background_tasks=%d",
            len(validate_dict),
            sum(len(items) for items in validate_dict.values()),
            len(validate_ok_dict),
            len(clientpool._pool),
            len(clientpool.active_uids),
            background_task_count(),
        )


def queue_memory_observer():
    global _observer_task
    if MEMORY_OBSERVE_INTERVAL <= 0:
        return None
    if _observer_task and not _observer_task.done():
        return _observer_task
    _observer_task = asyncio.get_event_loop().create_task(_memory_observer())

    def _release_task(done: asyncio.Task):
        global _observer_task
        if _observer_task is done:
            _observer_task = None
        if done.cancelled():
            return
        try:
            done.result()
        except Exception:
            logger.exception("memory observer failed")

    _observer_task.add_done_callback(_release_task)
    return _observer_task
