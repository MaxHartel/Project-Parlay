#a contest between two sides with odds
class simGame:

  def __init__(self,Game_ID, gameDate,FavoredTeam_ID,Underdog_ID,Fav_Implied_Win_P,UndD_Implied_Win_P,Winner_ID):
    self.date = gameDate
    self.gameID = Game_ID
    self.favoredTeam = FavoredTeam_ID
    self.underdog = Underdog_ID
    self.favWinP = Fav_Implied_Win_P
    self.undWinP = UndD_Implied_Win_P
    self.winner = Winner_ID