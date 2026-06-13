from typing import Dict, List
from ..util import questutils
from ..model.error import PanicError
import asyncio
import time
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from collections import defaultdict
from ..sdk.validator import remoteValidator, localValidator
from ..sdk.bsgamesdk import captch
from ..util.logger import instance as logger

@dataclass_json
@dataclass
class ValidateInfo:
    id: str = ""
    challenge: str = ""
    gt: str = ""
    userid: str = ""
    url: str = ""
    status: str = ""
    validate: str = ""

validate_dict: Dict[str, List[ValidateInfo]] = defaultdict(list)
validate_ok_dict: Dict[str, ValidateInfo] = {}
_validate_queue_times: Dict[str, List[float]] = defaultdict(list)
_validate_ok_times: Dict[str, float] = {}
_pending_validate_times: Dict[str, float] = {}

VALIDATE_PENDING_TTL = 180
VALIDATE_OK_TTL = 300
VALIDATE_QUEUE_MAX_SIZE = 5

def cleanup_validate_cache():
    now = time.time()

    for qid in list(validate_dict.keys()):
        queue = validate_dict[qid]
        times = _validate_queue_times[qid]
        if len(times) < len(queue):
            times = [now] * (len(queue) - len(times)) + times
        elif len(times) > len(queue):
            times = times[-len(queue):]
        _validate_queue_times[qid] = times
        kept = [
            (item, created_at)
            for item, created_at in zip(queue, times)
            if created_at + VALIDATE_PENDING_TTL >= now
        ]
        if len(kept) > VALIDATE_QUEUE_MAX_SIZE:
            kept = kept[-VALIDATE_QUEUE_MAX_SIZE:]
        if kept:
            validate_dict[qid] = [item for item, _ in kept]
            _validate_queue_times[qid] = [created_at for _, created_at in kept]
        else:
            validate_dict.pop(qid, None)
            _validate_queue_times.pop(qid, None)

    for id in list(validate_ok_dict.keys()):
        created_at = _validate_ok_times.get(id, 0)
        if created_at + VALIDATE_OK_TTL < now:
            validate_ok_dict.pop(id, None)
            _validate_ok_times.pop(id, None)

    for id in list(_pending_validate_times.keys()):
        if _pending_validate_times[id] + VALIDATE_PENDING_TTL < now:
            _pending_validate_times.pop(id, None)
            validate_ok_dict.pop(id, None)
            _validate_ok_times.pop(id, None)

def push_validate(qid: str, info: ValidateInfo):
    cleanup_validate_cache()
    validate_dict[qid].append(info)
    _validate_queue_times[qid].append(time.time())
    if info.id:
        _pending_validate_times[info.id] = time.time()
    while len(validate_dict[qid]) > VALIDATE_QUEUE_MAX_SIZE:
        removed = validate_dict[qid].pop(0)
        _validate_queue_times[qid].pop(0)
        if removed.id:
            _pending_validate_times.pop(removed.id, None)

def pop_validate(qid: str):
    cleanup_validate_cache()
    if qid not in validate_dict or not validate_dict[qid]:
        return None
    if _validate_queue_times.get(qid):
        _validate_queue_times[qid].pop()
    info = validate_dict[qid].pop()
    if not validate_dict[qid]:
        validate_dict.pop(qid, None)
        _validate_queue_times.pop(qid, None)
    return info

def remove_validate(qid: str, id: str):
    if qid not in validate_dict:
        _pending_validate_times.pop(id, None)
        return
    for index, info in enumerate(validate_dict[qid]):
        if info.id == id:
            validate_dict[qid].pop(index)
            if index < len(_validate_queue_times.get(qid, [])):
                _validate_queue_times[qid].pop(index)
            break
    if not validate_dict[qid]:
        validate_dict.pop(qid, None)
        _validate_queue_times.pop(qid, None)
    _pending_validate_times.pop(id, None)

def set_validate_ok(id: str, info: ValidateInfo):
    cleanup_validate_cache()
    if id not in _pending_validate_times:
        validate_ok_dict.pop(id, None)
        _validate_ok_times.pop(id, None)
        return False
    validate_ok_dict[id] = info
    _validate_ok_times[id] = time.time()
    return True

def pop_validate_ok(id: str):
    cleanup_validate_cache()
    info = validate_ok_dict.pop(id, None)
    _validate_ok_times.pop(id, None)
    return info

def create_validator(qq):
    async def validator():
        return await Validator(qq)
    return validator

async def Validator(qq):
    info = None
    for validator in [remoteValidator, localValidator, lambda: manualValidator(qq)]:
        try:
            info = await validator()
            if info:
                break
        except Exception as e:
            logger.exception(e)
    if not info:
        raise PanicError("验证码验证超时")
    return info

async def manualValidator(qq):

    if not manual_validator_enabled:
        raise PanicError("manual validator disabled")

    logger.info('use manual validator')

    cap = await captch()
    challenge = cap['challenge']
    gt = cap['gt']
    userid = cap['gt_user_id']

    id = questutils.create_quest_token()
    url = f"/daily/validate?id={id}&captcha_type=1&challenge={challenge}&gt={gt}&userid={userid}&gs=1"
    push_validate(qq, ValidateInfo(
            id=id,
            challenge=challenge,
            gt=gt,
            userid=userid,
            url=url,
            status="need validate"
    ))
    info = None
    try:
        for _ in range(120):
            validate = pop_validate_ok(id)
            if not validate:
                await asyncio.sleep(1)
            else:
                info = {
                    "challenge": validate.challenge,
                    "gt_user_id": validate.userid,
                    "validate" : validate.validate
                }
                break
    finally:
        remove_validate(qq, id)
        validate = pop_validate_ok(id)
        if validate and info is None:
            info = {
                "challenge": validate.challenge,
                "gt_user_id": validate.userid,
                "validate" : validate.validate
            }
    return info

manual_validator_enabled = False

def enable_manual_validator():
    global manual_validator_enabled
    if manual_validator_enabled:
        return
    manual_validator_enabled = True

    from ..module.accountmgr import instance as usermgr
    usermgr_load_legacy = usermgr.load
    def usermgr_load(qid: str, readonly=False):
        result = usermgr_load_legacy(qid, readonly=readonly)
        accountmgr_load_legacy = result.load
        def accountmgr_load(account: str = "", readonly=False, force_use_all=False):
            result = accountmgr_load_legacy(account=account, readonly=readonly, force_use_all=force_use_all)
            async def post_login():
                push_validate(qid, ValidateInfo(status="ok"))
            account_aenter_legacy = result._do_aenter
            async def account_aenter():
                res = await account_aenter_legacy()
                if not res.readonly:
                    res.client.session.sdk.append_post_login(post_login)
                    res.client.session.sdk.captchaVerifier = create_validator(qid)
                return res

            result._do_aenter = account_aenter
            return result
        result.load = accountmgr_load
        return result
    usermgr.load = usermgr_load
