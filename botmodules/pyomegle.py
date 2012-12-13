import botmodules.omegle as omegle

class omevent(omegle.EventHandler):
    def connected(self, chat, var):
        omevent.bot.irccontext.privmsg(omevent.e.source, "Connected to omegle user")

    def gotMessage(self, chat, message):
        message = "[ {} ]".format(message[0]).replace("\n", " | ")
        omevent.bot.irccontext.privmsg(omevent.e.source, message)

    def strangerDisconnected(self,chat,var):
        omevent.bot.irccontext.privmsg(omevent.e.source, "Stranger disconnected - Terminating")
        chat.terminate()

    def typing(self,chat,var):
        pass
        #omevent.bot.irccontext.privmsg(omevent.e.source, "Typing...")

    def stoppedTyping(self,chat,var):
        pass
        #omevent.bot.irccontext.privmsg(omevent.e.source, "Stopped Typing...")


def startomegle (self, e):
    omevent.bot = self
    omevent.e = e
    if self.omegleinstance:
        self.omegleinstance.disconnect()
    self.omegleinstance = omegle.OmegleChat()
    self.omegleinstance.connect_events(omevent())
    self.omegleinstance.connect(threaded=True)
    #self.omegleinstance.waitForTerminate()
startomegle.command = "!omegle"

def omeglesay (self, e):
    self.omegleinstance.say(e.input)
omeglesay.command = "!say"

def omegledc (self,e):
    self.omegleinstance.disconnect()
    e.output = "Omegle disconnected"
    return e
omegledc.command = "!odisconnect"
