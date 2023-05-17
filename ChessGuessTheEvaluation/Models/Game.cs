using Google.Cloud.Firestore;
using System.ComponentModel.DataAnnotations;

namespace ChessGuessTheEvaluation.Models
{
    [FirestoreData]
    public class Game
    {
        public int GameId { get; set; }

        [FirestoreProperty]
        [Required]
        public int WhiteElo { get; set; }
        
        [FirestoreProperty]
        [Required]
        public int BlackElo { get; set; }
        
        [FirestoreProperty]
        [Required]
        public string GameString { get; set; }
    }
}
