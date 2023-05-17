using ChessGuessTheEvaluation.Interface;
using ChessGuessTheEvaluation.Models;
using Google.Cloud.Firestore;
using Newtonsoft.Json;
using System.Security.Cryptography;

namespace ChessGuessTheEvaluation.DataAcess
{
    
    public class GameDataAccessLayer : ReadGame
    {
        string projectId;
        FirestoreDb firestoreDb;
        public GameDataAccessLayer()
        {
            string dbFilePath = "C:\\Users\\Jonathan L\\Desktop\\Code\\ChessTheElo\\chessguesstheelo-firebase-adminsdk-17z5u-2ece44e9df.json";
            Environment.SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", dbFilePath);
            projectId = "chessguesstheelo";
            firestoreDb = FirestoreDb.Create(projectId);
        }
        public async Task<Game> GetRandomGame()
        {
            Random rnd = new Random();
            try
            {
                //random number needs to go -- though i dont think firebase has a deafult way of getting a random entry
                Query gameQuery = firestoreDb.Collection("Games").WhereEqualTo("GameID", rnd.Next(70));
                QuerySnapshot orderQuerySnapshot = await gameQuery.GetSnapshotAsync();
                Game randGame = new Game();
                if (orderQuerySnapshot.Documents[0].Exists)
                {
                    Dictionary<string, object> dictonary = orderQuerySnapshot.Documents[0].ToDictionary();
                    string json = JsonConvert.SerializeObject(dictonary);
                    randGame = JsonConvert.DeserializeObject<Game>(json);
                    randGame.GameId = orderQuerySnapshot.Documents[0].GetValue<int>("GameID");
                    randGame.WhiteElo = orderQuerySnapshot.Documents[0].GetValue<int>("WhiteElo");
                    randGame.BlackElo = orderQuerySnapshot.Documents[0].GetValue<int>("BlackElo");
                    randGame.GameString = orderQuerySnapshot.Documents[0].GetValue<string>("GameString");
                }
                return randGame;
            }
            catch (Exception)
            {
                throw;
            }

        }
    }
}
