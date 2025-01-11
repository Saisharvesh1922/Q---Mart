class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self):
        """
        Convert the transaction to a dictionary.
        This will be useful for serializing it into a JSON format.
        """
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount
        }
