class User:
    def __init__(self, ID, Email, PhoneNum, Username, LastSeen):
        self.ID = ID
        self.Email = Email
        self.PhoneNum = PhoneNum
        self.Username = Username
        self.LastSeen = LastSeen

    def __str__(self):
        return f"User {self.ID} - {self.Username}: Last Seen: {self.LastSeen}"