class Watch:
    def __init__(self, ID, UserID, Username, LastNotify):
        self.ID = ID
        self.UserID = UserID
        self.Username = Username
        self.LastNotify = LastNotify


    def __str__(self):
        return f"Watch {self.ID} - Watch for UID {self.UserID} on player {self.Username} - Last Notified: {self.LastNotify}"
