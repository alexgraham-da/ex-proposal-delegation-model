
class SYMPHONY:
    InboundDirectMessage = 'SymphonyIntegration.InboundDirectMessage.InboundDirectMessage'
    InboundElementAction = 'SymphonyIntegration.InboundElementAction.InboundElementAction'
    OutboundMessage = 'SymphonyIntegration.OutboundMessage:OutboundMessage'
    UserStream = 'Symphony:UserStream'

class COMPANY:
    CompanySymphony = 'Symphony:CompanySymphony'
    Employee = 'Model.Company:Employee'

class PROPOSAL:
    Proposal = 'Model.Proposal:Proposal'
    Agreement = 'Model.Proposal:Agreement'
    DelegatedProposal = 'Model.Proposal:DelegatedProposal'

class NOTIFICATION:
    Notification = 'Model.Notification:Notification'

    def __init__(self, cid, cdata):
        self.cid = cid
        self.receiver = cdata['receiver']
        self.sender = cdata['sender']
        self.message = cdata['message']

    @classmethod
    def create(cls, receiver, sender, message):
        cdata = {
            receiver: receiver,
            sender: sender,
            message: message
        }
        cls(None, cdata)

    # def getReceiver(self):
    #     return self.receiver
    # def getSender(self):
    #     return self.sender
    # def getMessage(self):
    #     return self.message

    # sender (party)
    # receiver
    # message
