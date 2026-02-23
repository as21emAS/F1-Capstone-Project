import { Link } from "react-router-dom";
import FaultyTerminal from "../components/FaultyTerminal"; 
import FuzzyText from "../components/FuzzyText"; 
import "./NotFound.css";

const NotFound = () => {
  return (
    <div className="notfound-container">
      
      {/* 1. Terminal Background */}
      <div className="notfound-terminal-wrapper">
        <FaultyTerminal
          scale={1}
          digitSize={2.7}
          scanlineIntensity={0.5}
          glitchAmount={1.3}
          flickerAmount={1}
          noiseAmp={1}
          chromaticAberration={0}
          dither={0}
          curvature={0.1}
          tint="#b02700"
          mouseReact
          mouseStrength={0.5}
          brightness={0.6}
        />
      </div>

      {/* Error 404 Text */}
      <div className="notfound-text-wrapper">
        <div className="notfound-text">
          <FuzzyText 
            baseIntensity={0.2}
            hoverIntensity={0.5}
            enableHover
          >
            404
          </FuzzyText>
        </div>
      </div>

      {/* 3. Bottom Centered Button */}
      <div className="notfound-footer">
        <Link to="/" className="notfound-btn">
          Return to Dashboard
        </Link>
      </div>

    </div>
  );
};

export default NotFound;
