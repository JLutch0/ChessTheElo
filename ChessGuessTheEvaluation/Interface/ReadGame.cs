using ChessGuessTheEvaluation.Models;

namespace ChessGuessTheEvaluation.Interface
{
    public interface ReadGame
    {
        public Task<Game> GetRandomGame();
    }
}
