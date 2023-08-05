import logging
import pydle

from arrnounced import irc_modes
from arrnounced import message_handler

from arrnounced.eventloop_utils import eventloop_util

logger = logging.getLogger("IRC")


class IRC(irc_modes.ModesFixer):
    RECONNECT_MAX_ATTEMPTS = None

    def __init__(self, tracker, event_loop):
        super().__init__(tracker.config.irc_nickname, eventloop=event_loop)
        self.tracker = tracker

    async def connect(self, *args, **kwargs):
        try:
            await super().connect(*args, **kwargs)
        except OSError as e:
            logger.error("%s: %s", type(e).__name__, e)
            await self.on_disconnect(expected=False)

    # Request channel invite or join channel
    async def attempt_join_channel(self):
        if self.tracker.config.irc_invite_cmd is None:
            for channel in self.tracker.config.user_channels:
                logger.info("Joining %s", channel)
                await self.join(channel)
        else:
            logger.info("%s: Requesting invite", self.tracker.config.short_name)
            await self.message(
                self.tracker.config.irc_inviter, self.tracker.config.irc_invite_cmd
            )

    async def on_connect(self):
        logger.info("Connected to: %s", self.tracker.config.irc_server)
        await super().on_connect()

        if self.tracker.config.irc_ident_password is None:
            await self.attempt_join_channel()
        else:
            logger.info("Identifying with NICKSERV")
            await self.rawmsg(
                "PRIVMSG",
                "NICKSERV",
                "IDENTIFY",
                self.tracker.config.irc_ident_password,
            )

    async def on_raw(self, message):
        await super().on_raw(message)

        if message.command == 221 and "+r" in message._raw:
            logger.info("Identified with NICKSERV (221)")
            await self.attempt_join_channel()

    async def on_raw_900(self, message):
        logger.info("Identified with NICKSERV (900)")
        await self.attempt_join_channel()

    async def on_message(self, target, source, message):
        await message_handler.on_message(self.tracker, source, target.lower(), message)

    async def on_invite(self, channel, by):
        logger.info("%s invited us to join %s", by, channel)
        if channel in self.tracker.config.irc_channels:
            await self.join(channel)
        else:
            logger.warning(
                "Skipping join. %s is not in irc_channels list or specified in XML tracker configuration.",
                channel,
            )


pool = pydle.ClientPool()
eventloop_util.set_eventloop(pool.eventloop)
clients = []


def get_stop_tasks():
    logger.info("Stopping IRC client(s)")
    global clients
    for client in clients:
        # TODO: quit("Arrnounced out"). Capture Ctrl-C and close threads
        yield client.disconnect(expected=True)


def run(trackers):
    global pool, clients

    for tracker in trackers.values():
        logger.info(
            "Connecting to server: %s:%d %s",
            tracker.config.irc_server,
            tracker.config.irc_port,
            ", ".join(tracker.config.user_channels),
        )

        client = IRC(tracker, pool.eventloop)

        clients.append(client)
        try:
            pool.connect(
                client,
                hostname=tracker.config.irc_server,
                port=tracker.config.irc_port,
                tls=tracker.config.irc_tls,
                tls_verify=tracker.config.irc_tls_verify,
            )
        except Exception:
            logger.exception("Error while connecting to: %s", tracker.config.irc_server)

    try:
        pool.handle_forever()
    except Exception:
        logger.exception("Exception pool.handle_forever:")
