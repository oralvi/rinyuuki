from rin import sucmd
from rin.typing import CommandSession
from rin.util import escape

@sucmd('取码', force_private=False)
async def get_cqcode(session: CommandSession):
    await session.send(escape(str(session.current_arg)))
