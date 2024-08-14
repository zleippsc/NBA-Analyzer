import { useState } from "react";
import Alert from "./Alert";
import PlayerNames from "../PlayerNames";
import { predict } from "../api";

const PlayerEnter = () => {
  const [starPlayer, setStarPlayer] = useState("");
  const [secondPlayer, setSecondPlayer] = useState("");
  const [thirdPlayer, setThirdPlayer] = useState("");
  const [fourthPlayer, setFourthPlayer] = useState("");
  const [fifthPlayer, setFifthPlayer] = useState("");
  const [alertMessage, setAlertMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const team = [
      starPlayer,
      secondPlayer,
      thirdPlayer,
      fourthPlayer,
      fifthPlayer,
    ];
    setSuccessMessage("");
    for (let player of team) {
      if (!PlayerNames[player]) {
        setAlertMessage(
          `"${player}" is not recognized. Maybe check your spelling?`
        );
        return;
      }
    }
    setAlertMessage("");
    try {
      const response = await predict(team);
      let pred = response.prediction;
      pred = Math.round(pred * 1000) / 1000;
      setSuccessMessage(
        `Estimated win percentage: ${pred} (${Math.round(
          pred * 82
        )}-${Math.round((1 - pred) * 82)})`
      );
    } catch (error) {
      setAlertMessage("Error making prediction.");
    }
  };

  return (
    <div className="player-enter">
      <h2>Enter Starting Five</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter star player"
          required
          value={starPlayer}
          onChange={(e) => setStarPlayer(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter second player"
          required
          value={secondPlayer}
          onChange={(e) => setSecondPlayer(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter third player"
          required
          value={thirdPlayer}
          onChange={(e) => setThirdPlayer(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter fourth player"
          required
          value={fourthPlayer}
          onChange={(e) => setFourthPlayer(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter fifth player"
          required
          value={fifthPlayer}
          onChange={(e) => setFifthPlayer(e.target.value)}
        />
        <button>Generate Prediction</button>
        {alertMessage && (
          <Alert message={alertMessage} type="alert alert-danger" />
        )}
        {successMessage && (
          <Alert message={successMessage} type="alert alert-success" />
        )}
      </form>
    </div>
  );
};

export default PlayerEnter;
