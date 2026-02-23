import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { Card } from "../components/Card";
import "./NotFound.css";

const NotFound = () => {
  const navigate = useNavigate();
  const [scatteredText, setScatteredText] = useState<{ id: number; top: string; left: string; delay: string }[]>([]);

  useEffect(() => {
    // Generate random positions
    const generated = Array.from({ length: 10 }).map((_, i) => ({
      id: i,
      // Keep vertical position between 5% and 95%
      top: `${Math.floor(Math.random() * 90 + 5)}%`,
      // Keep horizontal position between 10% and 90% to avoid overlapping the checkered borders
      left: `${Math.floor(Math.random() * 80 + 10)}%`,
      // Randomize when the glitch animation starts for each text
      delay: `${(Math.random() * 5).toFixed(2)}s`, 
    }));
    setScatteredText(generated);
  }, []);

  return (
    <div className="notfound-container">
      <div className="crt-overlay"></div>

      {/* ── Scattered "POSITION LOST" Text ── */}
      {scatteredText.map((item) => (
        <p
          key={item.id}
          className="scattered-error"
          style={{
            top: item.top,
            left: item.left,
            animationDelay: item.delay,
          }}
        >
          POSITION LOST
        </p>
      ))}

      {/* ── Centered 404 Content ── */}
      <div className="notfound-content">
        <h1 className="error-code">404</h1>
      </div>

      {/* ── Action Card ── */}
      <div className="notfound-actions">
        <Card 
          variant="ghost" 
          onClick={() => navigate("/")}
          className="clickable-404-card"
        >
          <Card.Header title="ERROR 404 PAGE NOT FOUND" badge="SYSTEM" />
          <Card.Body>
            Click here to return to main Dashboard.
          </Card.Body>
        </Card>
      </div>
    </div>
  );
};

export default NotFound;